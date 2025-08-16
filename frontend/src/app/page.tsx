import TweetDashboard from "@/components/tweet-dashboard"

export default function Home() {
  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold mb-4">Bienvenido a la app de vacantes</h1>
      <TweetDashboard />
    </main>
  );
}
