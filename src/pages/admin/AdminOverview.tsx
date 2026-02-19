import { Users, BookOpen, CheckCircle2, Star, TrendingUp, Clock } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAdminStats, useAdminAnalytics, useModules } from "@/hooks/use-api";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from "recharts";

export default function AdminOverview() {
  const { data: stats } = useAdminStats();
  const { data: analytics } = useAdminAnalytics();
  const { data: modules = [] } = useModules();

  const roleData = analytics?.user_roles?.map(r => ({
    name: r.role === "student" ? "Étudiants" : r.role === "instructor" ? "Formateurs" : "Admins",
    value: r.count,
    fill: r.role === "student" ? "hsl(var(--accent))" : r.role === "instructor" ? "hsl(var(--info))" : "hsl(var(--warning))",
  })) || [];

  const moduleData = analytics?.popular_modules?.map(m => ({
    name: m.title.length > 12 ? m.title.slice(0, 12) + "…" : m.title,
    views: m.views,
  })) || [];

  const registrationData = analytics?.registrations_per_day?.map(d => ({
    day: new Date(d.date).toLocaleDateString("fr-FR", { weekday: "short" }),
    inscriptions: d.count,
  })) || [];

  const recentActivity = analytics?.recent_activity?.map(a => ({
    text: `${a.user} ${a.action}`,
    time: new Date(a.timestamp).toLocaleString("fr-FR"),
  })) || [];

  const kpis = [
    { label: "Utilisateurs", value: stats?.total_users ?? 0, sub: `+${stats?.users_growth ?? 0}% ce mois`, icon: Users, color: "text-accent" },
    { label: "Modules", value: stats?.total_modules ?? modules.length, sub: "Actifs: 100%", icon: BookOpen, color: "text-info" },
    { label: "Complétions", value: stats?.total_completions ?? 0, sub: `${stats?.completions_rate ?? 0}% taux`, icon: CheckCircle2, color: "text-success" },
    { label: "Note moyenne", value: stats?.average_rating ?? 0, sub: "sur 5", icon: TrendingUp, color: "text-warning" },
  ];

  return (
    <div className="p-6 space-y-6 animate-fade-in max-w-7xl mx-auto">
      <h1 className="text-2xl font-bold">Vue d'ensemble</h1>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {kpis.map(k => (
          <Card key={k.label}>
            <CardContent className="p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-muted-foreground">{k.label}</span>
                <k.icon className={`h-4 w-4 ${k.color}`} />
              </div>
              <div className="text-2xl font-bold">{k.value}</div>
              <p className="text-xs text-muted-foreground">{k.sub}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader><CardTitle className="text-base">Inscriptions (7 jours)</CardTitle></CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={200}>
              <LineChart data={registrationData}>
                <XAxis dataKey="day" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Line type="monotone" dataKey="inscriptions" stroke="hsl(var(--accent))" strokeWidth={2} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle className="text-base">Modules populaires</CardTitle></CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={moduleData}>
                <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="views" fill="hsl(var(--info))" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader><CardTitle className="text-base">Répartition par rôle</CardTitle></CardHeader>
          <CardContent className="flex items-center justify-center">
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie data={roleData} cx="50%" cy="50%" outerRadius={70} innerRadius={40} dataKey="value" label={({ name, value }) => `${name}: ${value}`}>
                  {roleData.map((entry, i) => <Cell key={i} fill={entry.fill} />)}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle className="text-base">Activité récente</CardTitle></CardHeader>
          <CardContent>
            <div className="space-y-3">
              {recentActivity.length === 0 && <p className="text-sm text-muted-foreground">Aucune activité récente</p>}
              {recentActivity.map((a, i) => (
                <div key={i} className="flex items-start gap-3">
                  <div className="mt-1.5 h-2 w-2 rounded-full bg-accent flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm">{a.text}</p>
                    <p className="text-xs text-muted-foreground flex items-center gap-1"><Clock className="h-3 w-3" />{a.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
