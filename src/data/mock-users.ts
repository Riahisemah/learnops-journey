export interface User {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  password: string;
  role: "student" | "instructor" | "admin";
  status: "active" | "blocked";
  createdAt: string;
  lastLogin: string;
  progression: number;
  modulesCompleted: number[];
  badges: string[];
  avatar: string;
}

const now = new Date();
const daysAgo = (d: number) => new Date(now.getTime() - d * 86400000).toISOString();

export const mockUsers: User[] = [
  // Admins
  { id: "a1", first_name: "Alice", last_name: "Martin", email: "admin@devops.com", password: "Admin123!", role: "admin", status: "active", createdAt: daysAgo(90), lastLogin: daysAgo(0), progression: 100, modulesCompleted: [1,2,3,4], badges: ["first-lesson","quiz-master","devops-pro","mlops-expert"], avatar: "" },
  { id: "a2", first_name: "Bruno", last_name: "Garcia", email: "bruno@devops.com", password: "Admin123!", role: "admin", status: "active", createdAt: daysAgo(85), lastLogin: daysAgo(1), progression: 90, modulesCompleted: [1,2,3], badges: ["first-lesson","quiz-master","devops-pro"], avatar: "" },
  // Instructors
  { id: "i1", first_name: "Claire", last_name: "Dubois", email: "claire@devops.com", password: "Instr123!", role: "instructor", status: "active", createdAt: daysAgo(60), lastLogin: daysAgo(0), progression: 85, modulesCompleted: [1,2,3], badges: ["first-lesson","quiz-master"], avatar: "" },
  { id: "i2", first_name: "David", last_name: "Leroy", email: "david@devops.com", password: "Instr123!", role: "instructor", status: "active", createdAt: daysAgo(55), lastLogin: daysAgo(2), progression: 70, modulesCompleted: [1,2], badges: ["first-lesson"], avatar: "" },
  { id: "i3", first_name: "Emma", last_name: "Bernard", email: "emma@devops.com", password: "Instr123!", role: "instructor", status: "active", createdAt: daysAgo(50), lastLogin: daysAgo(3), progression: 60, modulesCompleted: [1,2], badges: ["first-lesson"], avatar: "" },
  // Students
  { id: "s1", first_name: "Marie", last_name: "Dupont", email: "marie@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(30), lastLogin: daysAgo(0), progression: 75, modulesCompleted: [1,2,3], badges: ["first-lesson","quiz-master"], avatar: "" },
  { id: "s2", first_name: "Jean", last_name: "Moreau", email: "jean@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(28), lastLogin: daysAgo(1), progression: 55, modulesCompleted: [1,2], badges: ["first-lesson"], avatar: "" },
  { id: "s3", first_name: "Sophie", last_name: "Laurent", email: "sophie@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(25), lastLogin: daysAgo(0), progression: 90, modulesCompleted: [1,2,3], badges: ["first-lesson","quiz-master","devops-pro"], avatar: "" },
  { id: "s4", first_name: "Pierre", last_name: "Thomas", email: "pierre@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(22), lastLogin: daysAgo(2), progression: 40, modulesCompleted: [1], badges: ["first-lesson"], avatar: "" },
  { id: "s5", first_name: "Léa", last_name: "Robert", email: "lea@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(20), lastLogin: daysAgo(1), progression: 65, modulesCompleted: [1,2], badges: ["first-lesson"], avatar: "" },
  { id: "s6", first_name: "Lucas", last_name: "Richard", email: "lucas@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(18), lastLogin: daysAgo(3), progression: 30, modulesCompleted: [1], badges: ["first-lesson"], avatar: "" },
  { id: "s7", first_name: "Camille", last_name: "Durand", email: "camille@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(15), lastLogin: daysAgo(0), progression: 85, modulesCompleted: [1,2,3], badges: ["first-lesson","quiz-master"], avatar: "" },
  { id: "s8", first_name: "Hugo", last_name: "Petit", email: "hugo@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(12), lastLogin: daysAgo(4), progression: 20, modulesCompleted: [], badges: [], avatar: "" },
  { id: "s9", first_name: "Chloé", last_name: "Roux", email: "chloe@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(10), lastLogin: daysAgo(1), progression: 50, modulesCompleted: [1,2], badges: ["first-lesson"], avatar: "" },
  { id: "s10", first_name: "Thomas", last_name: "Fournier", email: "thomas@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(8), lastLogin: daysAgo(0), progression: 45, modulesCompleted: [1], badges: ["first-lesson"], avatar: "" },
  { id: "s11", first_name: "Manon", last_name: "Girard", email: "manon@example.com", password: "Student1!", role: "student", status: "blocked", createdAt: daysAgo(7), lastLogin: daysAgo(5), progression: 10, modulesCompleted: [], badges: [], avatar: "" },
  { id: "s12", first_name: "Nathan", last_name: "Andre", email: "nathan@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(5), lastLogin: daysAgo(0), progression: 15, modulesCompleted: [], badges: [], avatar: "" },
  { id: "s13", first_name: "Julie", last_name: "Mercier", email: "julie@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(3), lastLogin: daysAgo(0), progression: 5, modulesCompleted: [], badges: [], avatar: "" },
  { id: "s14", first_name: "Antoine", last_name: "Blanc", email: "antoine@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(2), lastLogin: daysAgo(0), progression: 0, modulesCompleted: [], badges: [], avatar: "" },
  { id: "s15", first_name: "Laura", last_name: "Guerin", email: "laura@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(1), lastLogin: daysAgo(0), progression: 0, modulesCompleted: [], badges: [], avatar: "" },
];
