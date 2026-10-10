export default function Badge({
  children,
  tone = "lavender",
}: {
  children: React.ReactNode;
  tone?: "lavender" | "sunset" | "neutral";
}) {
  const tones = {
    lavender: "border-lavender-400/40 text-lavender-300",
    sunset: "border-sunset-400/40 text-sunset-400",
    neutral: "border-midnight-600 text-midnight-300",
  } as const;
  return <span className={`badge ${tones[tone]}`}>{children}</span>;
}
