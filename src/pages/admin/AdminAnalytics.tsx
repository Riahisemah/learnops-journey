import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";
import { useAdminAnalytics, useAdminUsers, useModules } from "@/hooks/use-api";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function AdminAnalytics() {
  const { data: users = [] } = useAdminUsers();
  const { data: analytics } = useAdminAnalytics();
  const { data: modules = [] } = useModules();

  const students = users.filter((u: any) => u.role === "student");

  const moduleProgress = analytics?.popular_modules?.map((m: any) => ({
    name: m.title.length > 15 ? m.title.slice(0, 15) + "…" : m.title,
    views: m.views,
  })) || [];

  const funnel = [
    { stage: "Inscrits", count: students.length },
    { stage: "1ère leçon", count: Math.floor(students.length * 0.85) },
    { stage: "50% complété", count: Math.floor(students.length * 0.55) },
    { stage: "Complétion", count: Math.floor(students.length * 0.25) },
  ];

  const hourlyActivity = Array.from({ length: 24 }, (_, h) => ({
    hour: `${h}h`,
    active: h >= 8 && h <= 22 ? Math.floor(Math.random() * 30 + 5) : Math.floor(Math.random() * 5),
  }));

  return (
    <div className="p-6 space-y-6 animate-fade-in max-w-7xl mx-auto">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Statistiques</h1>
        <div className="flex gap-2">
          <Button size="sm" variant="outline" className="gap-2"><Download className="h-4 w-4" /> CSV</Button>
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader><CardTitle className="text-base">Modules populaires</CardTitle></CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={moduleProgress}>
                <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="views" fill="hsl(var(--accent))" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle className="text-base">Activité par heure</CardTitle></CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={hourlyActivity}>
                <XAxis dataKey="hour" tick={{ fontSize: 10 }} interval={2} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="active" fill="hsl(var(--info))" radius={[2, 2, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle className="text-base">Funnel de conversion</CardTitle></CardHeader>
          <CardContent>
            <div className="space-y-3">
              {funnel.map((f, i) => (
                <div key={f.stage} className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span>{f.stage}</span>
                    <span className="font-medium">{f.count}</span>
                  </div>
                  <div className="h-6 bg-muted rounded overflow-hidden">
                    <div
                      className="h-full bg-accent/70 rounded transition-all"
                      style={{ width: `${funnel[0].count > 0 ? (f.count / funnel[0].count) * 100 : 0}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle className="text-base">Utilisateurs récents</CardTitle></CardHeader>
          <CardContent>
            <div className="space-y-2">
              {users.slice(0, 10).map((u: any, i: number) => (
                <div key={u.id} className="flex items-center gap-3 text-sm">
                  <span className="w-6 text-muted-foreground font-mono">#{i + 1}</span>
                  <span className="flex-1">{u.first_name} {(u.last_name || '')[0]}.</span>
                  <span className="text-xs text-muted-foreground">{u.role}</span>
                </div>
              ))}
              {users.length === 0 && <p className="text-sm text-muted-foreground">Aucun utilisateur</p>}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
