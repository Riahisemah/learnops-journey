import { Users, BookOpen, CheckCircle2, Star, TrendingUp, Clock } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from "@/contexts/AuthContext";
import { modules } from "@/data/course-data";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from "recharts";

export default function AdminOverview() {
  const { users } = useAuth();
  const students = users.filter(u => u.role === "student");
  const instructors = users.filter(u => u.role === "instructor");
  const admins = users.filter(u => u.role === "admin");
  const avgProg = Math.round(students.reduce((a, s) => a + s.progression, 0) / (students.length || 1));
  const completions = students.filter(s => s.progression === 100).length;
  const completionRate = Math.round((completions / (students.length || 1)) * 100);

  const roleData = [
    { name: "Étudiants", value: students.length, fill: "hsl(var(--accent))" },
    { name: "Formateurs", value: instructors.length, fill: "hsl(var(--info))" },
    { name: "Admins", value: admins.length, fill: "hsl(var(--warning))" },
  ];

  const moduleData = modules.map(m => ({
    name: m.title.length > 12 ? m.title.slice(0, 12) + "…" : m.title,
    students: Math.floor(Math.random() * students.length) + 1,
  }));

  const last7Days = Array.from({ length: 7 }, (_, i) => {
    const d = new Date();
    d.setDate(d.getDate() - (6 - i));
    return { day: d.toLocaleDateString("fr-FR", { weekday: "short" }), inscriptions: Math.floor(Math.random() * 5) + 1 };
  });

  const recentActivity = [
    { text: "Sophie L. a complété le Module 3", time: "Il y a 5min" },
    { text: "Nouveau quiz ajouté par Admin", time: "Il y a 1h" },
    { text: "Jean M. s'est inscrit", time: "Il y a 2h" },
    { text: "Marie D. a obtenu le badge quiz-master", time: "Il y a 3h" },
    { text: "Lucas R. a commencé le Module 2", time: "Il y a 5h" },
  ];

  const kpis = [
    { label: "Utilisateurs", value: users.length.toLocaleString(), sub: `+${Math.floor(Math.random() * 15 + 5)}% ce mois`, icon: Users, color: "text-accent" },
    { label: "Modules", value: modules.length, sub: "Actifs: 100%", icon: BookOpen, color: "text-info" },
    { label: "Complétions", value: completions, sub: `${completionRate}% taux`, icon: CheckCircle2, color: "text-success" },
    { label: "Progression moy.", value: `${avgProg}%`, sub: "+3% ce mois", icon: TrendingUp, color: "text-warning" },
  ];

  return (
    <div className="p-6 space-y-6 animate-fade-in max-w-7xl mx-auto">
      <h1 className="text-2xl font-bold">Vue d'ensemble</h1>

      {/* KPIs */}
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

      {/* Charts row */}
      <div className="grid lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader><CardTitle className="text-base">Inscriptions (7 jours)</CardTitle></CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={200}>
              <LineChart data={last7Days}>
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
                <Bar dataKey="students" fill="hsl(var(--info))" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Pie chart */}
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

        {/* Recent activity */}
        <Card>
          <CardHeader><CardTitle className="text-base">Activité récente</CardTitle></CardHeader>
          <CardContent>
            <div className="space-y-3">
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
