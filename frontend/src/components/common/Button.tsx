import { type ButtonHTMLAttributes } from "react";

export default function Button({
  variant = "primary",
  className = "",
  ...rest
}: ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary";
}) {
  const cls = variant === "primary" ? "btn-primary" : "btn-secondary";
  return <button {...rest} className={`${cls} ${className}`} />;
}
