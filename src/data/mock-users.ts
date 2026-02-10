export interface User {
  id: string;
  firstName: string;
  lastName: string;
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
  { id: "a1", firstName: "Alice", lastName: "Martin", email: "admin@devops.com", password: "Admin123!", role: "admin", status: "active", createdAt: daysAgo(90), lastLogin: daysAgo(0), progression: 100, modulesCompleted: [1,2,3,4], badges: ["first-lesson","quiz-master","devops-pro","mlops-expert"], avatar: "" },
  { id: "a2", firstName: "Bruno", lastName: "Garcia", email: "bruno@devops.com", password: "Admin123!", role: "admin", status: "active", createdAt: daysAgo(85), lastLogin: daysAgo(1), progression: 90, modulesCompleted: [1,2,3], badges: ["first-lesson","quiz-master","devops-pro"], avatar: "" },
  // Instructors
  { id: "i1", firstName: "Claire", lastName: "Dubois", email: "claire@devops.com", password: "Instr123!", role: "instructor", status: "active", createdAt: daysAgo(60), lastLogin: daysAgo(0), progression: 85, modulesCompleted: [1,2,3], badges: ["first-lesson","quiz-master"], avatar: "" },
  { id: "i2", firstName: "David", lastName: "Leroy", email: "david@devops.com", password: "Instr123!", role: "instructor", status: "active", createdAt: daysAgo(55), lastLogin: daysAgo(2), progression: 70, modulesCompleted: [1,2], badges: ["first-lesson"], avatar: "" },
  { id: "i3", firstName: "Emma", lastName: "Bernard", email: "emma@devops.com", password: "Instr123!", role: "instructor", status: "active", createdAt: daysAgo(50), lastLogin: daysAgo(3), progression: 60, modulesCompleted: [1,2], badges: ["first-lesson"], avatar: "" },
  // Students
  { id: "s1", firstName: "Marie", lastName: "Dupont", email: "marie@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(30), lastLogin: daysAgo(0), progression: 75, modulesCompleted: [1,2,3], badges: ["first-lesson","quiz-master"], avatar: "" },
  { id: "s2", firstName: "Jean", lastName: "Moreau", email: "jean@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(28), lastLogin: daysAgo(1), progression: 55, modulesCompleted: [1,2], badges: ["first-lesson"], avatar: "" },
  { id: "s3", firstName: "Sophie", lastName: "Laurent", email: "sophie@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(25), lastLogin: daysAgo(0), progression: 90, modulesCompleted: [1,2,3], badges: ["first-lesson","quiz-master","devops-pro"], avatar: "" },
  { id: "s4", firstName: "Pierre", lastName: "Thomas", email: "pierre@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(22), lastLogin: daysAgo(2), progression: 40, modulesCompleted: [1], badges: ["first-lesson"], avatar: "" },
  { id: "s5", firstName: "Léa", lastName: "Robert", email: "lea@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(20), lastLogin: daysAgo(1), progression: 65, modulesCompleted: [1,2], badges: ["first-lesson"], avatar: "" },
  { id: "s6", firstName: "Lucas", lastName: "Richard", email: "lucas@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(18), lastLogin: daysAgo(3), progression: 30, modulesCompleted: [1], badges: ["first-lesson"], avatar: "" },
  { id: "s7", firstName: "Camille", lastName: "Durand", email: "camille@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(15), lastLogin: daysAgo(0), progression: 85, modulesCompleted: [1,2,3], badges: ["first-lesson","quiz-master"], avatar: "" },
  { id: "s8", firstName: "Hugo", lastName: "Petit", email: "hugo@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(12), lastLogin: daysAgo(4), progression: 20, modulesCompleted: [], badges: [], avatar: "" },
  { id: "s9", firstName: "Chloé", lastName: "Roux", email: "chloe@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(10), lastLogin: daysAgo(1), progression: 50, modulesCompleted: [1,2], badges: ["first-lesson"], avatar: "" },
  { id: "s10", firstName: "Thomas", lastName: "Fournier", email: "thomas@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(8), lastLogin: daysAgo(0), progression: 45, modulesCompleted: [1], badges: ["first-lesson"], avatar: "" },
  { id: "s11", firstName: "Manon", lastName: "Girard", email: "manon@example.com", password: "Student1!", role: "student", status: "blocked", createdAt: daysAgo(7), lastLogin: daysAgo(5), progression: 10, modulesCompleted: [], badges: [], avatar: "" },
  { id: "s12", firstName: "Nathan", lastName: "Andre", email: "nathan@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(5), lastLogin: daysAgo(0), progression: 15, modulesCompleted: [], badges: [], avatar: "" },
  { id: "s13", firstName: "Julie", lastName: "Mercier", email: "julie@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(3), lastLogin: daysAgo(0), progression: 5, modulesCompleted: [], badges: [], avatar: "" },
  { id: "s14", firstName: "Antoine", lastName: "Blanc", email: "antoine@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(2), lastLogin: daysAgo(0), progression: 0, modulesCompleted: [], badges: [], avatar: "" },
  { id: "s15", firstName: "Laura", lastName: "Guerin", email: "laura@example.com", password: "Student1!", role: "student", status: "active", createdAt: daysAgo(1), lastLogin: daysAgo(0), progression: 0, modulesCompleted: [], badges: [], avatar: "" },
];
