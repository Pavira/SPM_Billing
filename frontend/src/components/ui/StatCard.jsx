export default function StatCard({ title, value }) {
  return (
    <div className="bg-white rounded-2xl shadow p-4 md:p-6 hover:shadow-lg transition">
      <p className="text-gray-500 font-semibold text-xs md:text-sm">{title}</p>
      <h2 className="text-3xl md:text-5xl font-bold text-purple-700 mt-2">
        {value}
      </h2>
    </div>
  );
}
