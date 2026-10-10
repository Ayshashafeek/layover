import { type ReactNode } from "react";

export default function Card({
  children,
  className = "",
}: {
  children: ReactNode;
  className?: string;
}) {
  return <section className={`card p-5 animate-fade-up ${className}`}>{children}</section>;
}
