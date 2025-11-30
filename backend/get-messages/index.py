import json
import os
import psycopg2
from typing import Dict, Any

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    '''
    Business: Get all chat messages with user info and reactions
    Args: event with httpMethod, queryStringParameters (limit, offset)
          context with request_id
    Returns: HTTP response with messages array
    '''
    method: str = event.get('httpMethod', 'GET')
    
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '86400'
            },
            'body': ''
        }
    
    if method != 'GET':
        return {
            'statusCode': 405,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    params = event.get('queryStringParameters') or {}
    limit = int(params.get('limit', 20))
    offset = int(params.get('offset', 0))
    
    dsn = os.environ.get('DATABASE_URL')
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    
    cur.execute(f"""
        SELECT 
            m.id, m.text, m.created_at,
            u.id, u.username
        FROM t_p53416936_auxchat_energy_messa.messages m
        JOIN t_p53416936_auxchat_energy_messa.users u ON m.user_id = u.id
        ORDER BY m.created_at ASC
        LIMIT {limit} OFFSET {offset}
    """)
    
    rows = cur.fetchall()
    messages = []
    
    for row in rows:
        msg_id, text, created_at, user_id, username = row
        
        cur.execute(f"""
            SELECT emoji, COUNT(*) as count
            FROM t_p53416936_auxchat_energy_messa.message_reactions
            WHERE message_id = {msg_id}
            GROUP BY emoji
        """)
        
        reactions = [{'emoji': r[0], 'count': r[1]} for r in cur.fetchall()]
        
        cur.execute(f"""
            SELECT photo_url
            FROM t_p53416936_auxchat_energy_messa.user_photos
            WHERE user_id = {user_id}
            ORDER BY display_order ASC, created_at DESC
            LIMIT 1
        """)
        
        photo_row = cur.fetchone()
        user_avatar = photo_row[0] if photo_row else f'https://api.dicebear.com/7.x/avataaars/svg?seed={username}'
        
        messages.append({
            'id': msg_id,
            'text': text,
            'created_at': created_at.isoformat(),
            'user': {
                'id': user_id,
                'username': username,
                'avatar': user_avatar
            },
            'reactions': reactions
        })
    
    cur.close()
    conn.close()
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'isBase64Encoded': False,
        'body': json.dumps({'messages': messages})
    }