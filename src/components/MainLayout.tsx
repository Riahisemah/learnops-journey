import { Outlet } from "react-router-dom";
import { AppSidebar } from "@/components/AppSidebar";

export function MainLayout() {
  return (
    <div className="min-h-screen flex w-full">
      <AppSidebar />
      <main className="flex-1 lg:ml-0 pt-14 lg:pt-0">
        <Outlet />
      </main>
    </div>
  );
}
