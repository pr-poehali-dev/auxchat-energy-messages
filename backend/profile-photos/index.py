'''
Business: Manage user profile photo gallery (upload, list, delete)
Args: event with httpMethod, headers (X-User-Id), body for photo URLs
Returns: HTTP response with photos list or operation status
'''

import json
import os
import psycopg2
from typing import Dict, Any

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    method: str = event.get('httpMethod', 'GET')
    
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, X-User-Id',
                'Access-Control-Max-Age': '86400'
            },
            'body': ''
        }
    
    headers = event.get('headers', {})
    user_id_str = headers.get('X-User-Id') or headers.get('x-user-id')
    
    if not user_id_str:
        return {
            'statusCode': 401,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'X-User-Id header required'})
        }
    
    user_id = int(user_id_str)
    dsn = os.environ.get('DATABASE_URL')
    
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    
    if method == 'GET':
        query_params = event.get('queryStringParameters', {})
        target_user_id = query_params.get('userId', user_id)
        
        cur.execute(
            "SELECT id, photo_url, created_at FROM t_p53416936_auxchat_energy_messa.user_photos WHERE user_id = %s ORDER BY created_at DESC LIMIT 6",
            (target_user_id,)
        )
        rows = cur.fetchall()
        
        photos = [
            {'id': row[0], 'url': row[1], 'created_at': row[2].isoformat()}
            for row in rows
        ]
        
        cur.close()
        conn.close()
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'photos': photos})
        }
    
    if method == 'POST':
        body_data = json.loads(event.get('body', '{}'))
        photo_url = body_data.get('photoUrl', '').strip()
        
        if not photo_url:
            cur.close()
            conn.close()
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'photoUrl required'})
            }
        
        cur.execute(
            "SELECT COUNT(*) FROM t_p53416936_auxchat_energy_messa.user_photos WHERE user_id = %s",
            (user_id,)
        )
        count = cur.fetchone()[0]
        
        if count >= 6:
            cur.close()
            conn.close()
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Maximum 6 photos allowed'})
            }
        
        cur.execute(
            "INSERT INTO t_p53416936_auxchat_energy_messa.user_photos (user_id, photo_url) VALUES (%s, %s) RETURNING id",
            (user_id, photo_url)
        )
        photo_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'success': True, 'photoId': photo_id})
        }
    
    if method == 'DELETE':
        query_params = event.get('queryStringParameters', {})
        photo_id_str = query_params.get('photoId')
        
        if not photo_id_str:
            cur.close()
            conn.close()
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'photoId required'})
            }
        
        photo_id = int(photo_id_str)
        
        cur.execute(
            "DELETE FROM t_p53416936_auxchat_energy_messa.user_photos WHERE id = %s AND user_id = %s",
            (photo_id, user_id)
        )
        affected = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        
        if affected == 0:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Photo not found'})
            }
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'success': True})
        }
    
    cur.close()
    conn.close()
    return {
        'statusCode': 405,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'error': 'Method not allowed'})
    }
