import { useEffect, useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import Icon from '@/components/ui/icon';
import { toast } from 'sonner';

interface Message {
  id: number;
  senderId: number;
  receiverId: number;
  text: string;
  isRead: boolean;
  createdAt: string;
  sender: {
    username: string;
    avatarUrl: string | null;
  };
}

interface UserProfile {
  id: number;
  username: string;
  avatar: string;
  status: string;
}

export default function Chat() {
  const { userId } = useParams();
  const navigate = useNavigate();
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const currentUserId = localStorage.getItem('userId');

  useEffect(() => {
    loadProfile();
    loadMessages();
    const interval = setInterval(loadMessages, 3000);
    return () => clearInterval(interval);
  }, [userId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadProfile = async () => {
    try {
      const response = await fetch(
        `https://functions.poehali.dev/518f730f-1a8e-45ad-b0ed-e9a66c5a3784?user_id=${userId}`
      );
      const data = await response.json();
      setProfile(data);
    } catch (error) {
      toast.error('Ошибка загрузки профиля');
    }
  };

  const loadMessages = async () => {
    try {
      const response = await fetch(
        `https://functions.poehali.dev/0222e582-5c06-4780-85fa-c9145e5bba14?otherUserId=${userId}`,
        {
          headers: {
            'X-User-Id': currentUserId || '0'
          }
        }
      );
      const data = await response.json();
      setMessages(data.messages || []);
    } catch (error) {
      console.error('Error loading messages:', error);
    } finally {
      setLoading(false);
    }
  };

  const sendMessage = async () => {
    if (!newMessage.trim()) return;

    try {
      const response = await fetch(
        'https://functions.poehali.dev/0222e582-5c06-4780-85fa-c9145e5bba14',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-User-Id': currentUserId || '0'
          },
          body: JSON.stringify({
            receiverId: Number(userId),
            text: newMessage
          })
        }
      );

      if (response.ok) {
        setNewMessage('');
        loadMessages();
      } else {
        toast.error('Ошибка отправки сообщения');
      }
    } catch (error) {
      toast.error('Ошибка отправки сообщения');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="animate-spin">
          <Icon name="Loader2" size={32} />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-purple-950/20 to-background flex flex-col">
      <div className="bg-card/90 backdrop-blur border-b border-purple-500/20 p-4">
        <div className="container mx-auto max-w-4xl flex items-center gap-4">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => navigate('/')}
          >
            <Icon name="ArrowLeft" size={20} />
          </Button>

          {profile && (
            <button
              onClick={() => navigate(`/profile/${userId}`)}
              className="flex items-center gap-3 flex-1 hover:bg-accent/50 rounded-lg p-2 transition-colors"
            >
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white font-bold flex-shrink-0">
                {profile.avatar ? (
                  <img src={profile.avatar} alt={profile.username} className="w-full h-full rounded-full object-cover" />
                ) : (
                  profile.username[0]?.toUpperCase()
                )}
              </div>
              <div className="text-left">
                <p className="font-semibold">{profile.username}</p>
                <p className={`text-xs ${
                  profile.status === 'online' ? 'text-green-400' : 'text-muted-foreground'
                }`}>
                  {profile.status === 'online' ? 'Онлайн' : 'Не в сети'}
                </p>
              </div>
            </button>
          )}
        </div>
      </div>

      <div className="flex-1 container mx-auto max-w-4xl px-4 py-6 overflow-y-auto">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <p className="text-muted-foreground">Нет сообщений. Начните диалог!</p>
          </div>
        ) : (
          <div className="space-y-4">
            {messages.map((message) => {
              const isOwn = String(message.senderId) === String(currentUserId);
              return (
                <div
                  key={message.id}
                  className={`flex ${isOwn ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`max-w-[70%] ${isOwn ? 'order-2' : 'order-1'}`}>
                    <Card className={`p-3 ${
                      isOwn
                        ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                        : 'bg-card'
                    }`}>
                      <p className="break-words">{message.text}</p>
                      <p className={`text-xs mt-1 ${
                        isOwn ? 'text-purple-100' : 'text-muted-foreground'
                      }`}>
                        {new Date(message.createdAt).toLocaleTimeString('ru-RU', {
                          hour: '2-digit',
                          minute: '2-digit'
                        })}
                      </p>
                    </Card>
                  </div>
                </div>
              );
            })}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <div className="bg-card/90 backdrop-blur border-t border-purple-500/20 p-4">
        <div className="container mx-auto max-w-4xl flex gap-2">
          <textarea
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Написать сообщение..."
            className="flex-1 px-4 py-3 rounded-lg bg-background border border-border resize-none"
            rows={1}
          />
          <Button
            onClick={sendMessage}
            disabled={!newMessage.trim()}
            className="bg-gradient-to-r from-purple-500 to-pink-500 px-6"
          >
            <Icon name="Send" size={20} />
          </Button>
        </div>
      </div>
    </div>
  );
}
