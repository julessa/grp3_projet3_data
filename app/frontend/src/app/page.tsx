import SideNav from "@/components/SideNav";
import TopNav from "@/components/TopNav";
import AnalyzeInput from "@/components/AnalyzeInput";
import AnalysisResults from "@/components/AnalysisResults";

export default function PageTableauDeBord() {
  return (
    <div className="bg-ios-bg min-h-screen">
      <SideNav />
      <main className="ml-[260px] min-h-screen">
        <TopNav />
        <div className="p-8 max-w-7xl mx-auto">
          <AnalyzeInput />
          <AnalysisResults />
        </div>
      </main>
    </div>
  );
}
