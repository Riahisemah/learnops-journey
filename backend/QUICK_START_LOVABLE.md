# 🚀 Guide Rapide - Intégration Frontend Lovable

## 📦 Ce Qui a Changé

Le backend a été **mis à jour avec 22 nouveaux endpoints** pour être 100% compatible avec vos besoins.

---

## ✅ NOUVEAUX ENDPOINTS DISPONIBLES

### 1. Notifications (5 endpoints)
```
POST   /api/notifications
GET    /api/notifications/me
PUT    /api/notifications/{id}/read
DELETE /api/notifications/{id}
GET    /api/notifications/unread/count
```

### 2. Certificats (4 endpoints)
```
POST   /api/certificates/generate
GET    /api/certificates/me
GET    /api/certificates/{id}
DELETE /api/certificates/{id}
```

### 3. Commentaires (3 endpoints)
```
POST   /api/lessons/{id}/comments
GET    /api/lessons/{id}/comments
DELETE /api/comments/{id}
```

### 4. Recherche (1 endpoint)
```
GET    /api/search?q=docker
```

### 5. Favoris (4 endpoints)
```
POST   /api/bookmarks
GET    /api/bookmarks/me
DELETE /api/bookmarks/{id}
GET    /api/bookmarks/check
```

### 6. Progression (améliorée)
```
GET    /api/progress/me       → Calcul automatique + badges
POST   /api/progress/update   → Champs optionnels
```

---

## 🔧 SERVICES À CRÉER DANS LOVABLE

### 1. notificationService.ts

```typescript
// src/services/notificationService.ts
import httpClient from '@/lib/httpClient';
import { API_CONFIG } from '@/config/api';

export interface Notification {
  id: string;
  title: string;
  message: string;
  type: 'info' | 'success' | 'warning' | 'error';
  read: boolean;
  created_at: string;
}

export const notificationService = {
  async getMyNotifications(): Promise<Notification[]> {
    const { data } = await httpClient.get('/api/notifications/me');
    return data;
  },

  async markAsRead(id: string): Promise<void> {
    await httpClient.put(`/api/notifications/${id}/read`);
  },

  async deleteNotification(id: string): Promise<void> {
    await httpClient.delete(`/api/notifications/${id}`);
  },

  async getUnreadCount(): Promise<number> {
    const { data } = await httpClient.get('/api/notifications/unread/count');
    return data.count;
  },
};
```

### 2. certificateService.ts

```typescript
// src/services/certificateService.ts
import httpClient from '@/lib/httpClient';

export const certificateService = {
  async generate(): Promise<{ certificate_id: string; download_url: string }> {
    const { data } = await httpClient.post('/api/certificates/generate');
    return data;
  },

  async getMyCertificates(): Promise<any[]> {
    const { data } = await httpClient.get('/api/certificates/me');
    return data;
  },

  async download(id: string): Promise<any> {
    const { data } = await httpClient.get(`/api/certificates/${id}`);
    return data;
  },
};
```

### 3. commentService.ts

```typescript
// src/services/commentService.ts
import httpClient from '@/lib/httpClient';

export interface Comment {
  id: string;
  lesson_id: string;
  user_id: string;
  user_name: string;
  content: string;
  created_at: string;
}

export const commentService = {
  async addComment(lessonId: string, content: string): Promise<Comment> {
    const { data } = await httpClient.post(
      `/api/lessons/${lessonId}/comments`,
      { content }
    );
    return data;
  },

  async getComments(
    lessonId: string,
    skip = 0,
    limit = 50
  ): Promise<{ total: number; comments: Comment[] }> {
    const { data } = await httpClient.get(
      `/api/lessons/${lessonId}/comments`,
      { params: { skip, limit } }
    );
    return data;
  },

  async deleteComment(commentId: string): Promise<void> {
    await httpClient.delete(`/api/comments/${commentId}`);
  },
};
```

### 4. searchService.ts

```typescript
// src/services/searchService.ts
import httpClient from '@/lib/httpClient';

export const searchService = {
  async search(query: string, limit = 20) {
    const { data } = await httpClient.get('/api/search', {
      params: { q: query, limit },
    });
    return data;
  },
};
```

### 5. bookmarkService.ts

```typescript
// src/services/bookmarkService.ts
import httpClient from '@/lib/httpClient';

export const bookmarkService = {
  async add(
    resourceType: 'module' | 'lesson' | 'quiz',
    resourceId: string,
    title: string
  ) {
    const { data } = await httpClient.post('/api/bookmarks', {
      resource_type: resourceType,
      resource_id: resourceId,
      title,
    });
    return data;
  },

  async getMyBookmarks(resourceType?: string) {
    const { data } = await httpClient.get('/api/bookmarks/me', {
      params: resourceType ? { resource_type: resourceType } : {},
    });
    return data;
  },

  async remove(bookmarkId: string) {
    await httpClient.delete(`/api/bookmarks/${bookmarkId}`);
  },

  async check(resourceType: string, resourceId: string): Promise<boolean> {
    const { data } = await httpClient.get('/api/bookmarks/check', {
      params: { resource_type: resourceType, resource_id: resourceId },
    });
    return data.is_bookmarked;
  },
};
```

### 6. Mettre à jour progressService.ts

```typescript
// src/services/progressService.ts (mise à jour)
export const progressService = {
  async getMyProgress() {
    const { data } = await httpClient.get('/api/progress/me');
    // data contient maintenant : lessons_completed, total_lessons, badges automatiques
    return data;
  },

  async update(updates: {
    progression?: number;
    modules_completed?: number[];
    time_spent?: number;
  }) {
    // Tous les champs sont optionnels maintenant
    const { data } = await httpClient.post('/api/progress/update', updates);
    return data;
  },
};
```

---

## 🎨 COMPOSANTS UI À CRÉER

### 1. NotificationBell (Header)

```typescript
// src/components/NotificationBell.tsx
import { Bell } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import { notificationService } from '@/services/notificationService';

export function NotificationBell() {
  const { data: count } = useQuery({
    queryKey: ['notifications', 'unread-count'],
    queryFn: notificationService.getUnreadCount,
    refetchInterval: 30000, // Rafraîchir toutes les 30s
  });

  return (
    <button className="relative">
      <Bell className="h-6 w-6" />
      {count > 0 && (
        <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
          {count}
        </span>
      )}
    </button>
  );
}
```

### 2. CommentSection (Sous chaque leçon)

```typescript
// src/components/lesson/CommentSection.tsx
import { useState } from 'use';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { commentService } from '@/services/commentService';

export function CommentSection({ lessonId }: { lessonId: string }) {
  const [content, setContent] = useState('');
  const queryClient = useQueryClient();

  const { data } = useQuery({
    queryKey: ['comments', lessonId],
    queryFn: () => commentService.getComments(lessonId),
  });

  const addMutation = useMutation({
    mutationFn: (content: string) => commentService.addComment(lessonId, content),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['comments', lessonId] });
      setContent('');
    },
  });

  return (
    <div className="mt-8">
      <h3 className="text-xl font-bold mb-4">Commentaires ({data?.total || 0})</h3>
      
      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Ajouter un commentaire..."
        className="w-full p-3 border rounded mb-2"
      />
      
      <button
        onClick={() => addMutation.mutate(content)}
        disabled={!content.trim()}
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        Commenter
      </button>

      <div className="mt-6 space-y-4">
        {data?.comments.map((comment) => (
          <div key={comment.id} className="border-l-4 border-blue-500 pl-4">
            <div className="font-bold">{comment.user_name}</div>
            <div className="text-sm text-gray-500">
              {new Date(comment.created_at).toLocaleDateString()}
            </div>
            <p className="mt-2">{comment.content}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
```

### 3. SearchDialog (Cmd+K)

```typescript
// src/components/SearchDialog.tsx
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Dialog, DialogContent } from '@/components/ui/dialog';
import { searchService } from '@/services/searchService';
import { Search } from 'lucide-react';

export function SearchDialog() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const navigate = useNavigate();

  // Ouvrir avec Cmd+K
  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen(true);
      }
    };
    document.addEventListener('keydown', down);
    return () => document.removeEventListener('keydown', down);
  }, []);

  const handleSearch = async (q: string) => {
    if (q.length >= 2) {
      const data = await searchService.search(q);
      setResults(data);
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent>
        <div className="flex items-center gap-2 mb-4">
          <Search className="h-5 w-5 text-gray-400" />
          <input
            type="text"
            placeholder="Rechercher..."
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              handleSearch(e.target.value);
            }}
            className="flex-1 outline-none"
            autoFocus
          />
        </div>

        {results && (
          <div className="space-y-4">
            {results.results.modules.length > 0 && (
              <div>
                <h3 className="font-bold mb-2">Modules</h3>
                {results.results.modules.map((m) => (
                  <div
                    key={m.id}
                    onClick={() => {
                      navigate(`/modules/${m.id}`);
                      setOpen(false);
                    }}
                    className="p-2 hover:bg-gray-100 cursor-pointer rounded"
                  >
                    {m.title}
                  </div>
                ))}
              </div>
            )}
            {/* Répéter pour lessons et quizzes */}
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}
```

---

## 🎯 CHECKLIST D'INTÉGRATION

### Étape 1 : Services (1 heure)
- [ ] Créer `notificationService.ts`
- [ ] Créer `certificateService.ts`
- [ ] Créer `commentService.ts`
- [ ] Créer `searchService.ts`
- [ ] Créer `bookmarkService.ts`
- [ ] Mettre à jour `progressService.ts`

### Étape 2 : Hooks React Query (30 min)
- [ ] Ajouter hooks dans `use-api.ts` pour chaque service

### Étape 3 : Composants UI (2 heures)
- [ ] `NotificationBell` dans le header
- [ ] `CommentSection` sous les leçons
- [ ] `SearchDialog` (Cmd+K)
- [ ] Boutons favoris (icône étoile)
- [ ] Bouton "Générer certificat" sur page profil

### Étape 4 : Pages (1 heure)
- [ ] Page `/notifications`
- [ ] Page `/bookmarks` (Mes favoris)
- [ ] Section certificats dans `/profile`

### Étape 5 : Tests (30 min)
- [ ] Tester tous les nouveaux endpoints
- [ ] Vérifier les loading states
- [ ] Tester les erreurs

---

## 🔥 DÉMARRAGE RAPIDE

```bash
# 1. Backend déjà mis à jour dans le ZIP
cd backend
python seed_db.py
uvicorn app.main:app --reload

# 2. Frontend Lovable
# Copier les services ci-dessus dans src/services/
# Créer les composants UI
# Tester !
```

---

## 📚 DOCUMENTATION COMPLÈTE

- `docs/NEW_ENDPOINTS.md` - Tous les nouveaux endpoints en détail
- `docs/CHANGELOG_LOVABLE.md` - Changelog complet
- `API_REFERENCE.md` - Documentation API complète

---

## 💡 AIDE RAPIDE

**Backend ne démarre pas ?**
```bash
pip install -r requirements.txt
python seed_db.py
```

**Erreur 401 ?**
- Vérifier que le token est bien dans localStorage
- Re-login si nécessaire

**Endpoint introuvable ?**
- Vérifier Swagger UI : http://localhost:8000/docs
- Tous les endpoints y sont documentés

Bon développement ! 🚀
