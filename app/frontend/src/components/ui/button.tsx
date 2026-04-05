import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-xl text-sm font-semibold transition-all outline-none select-none active:scale-[0.97] disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-ios-blue text-white hover:brightness-110 shadow-ios-sm",
        outline: "border border-ios-border bg-ios-card text-ios-label hover:bg-ios-card-hover",
        secondary: "bg-ios-bg text-ios-label-secondary hover:bg-ios-card-hover",
        ghost: "text-ios-label-secondary hover:bg-ios-card-hover",
        destructive: "bg-ios-red/10 text-ios-red hover:bg-ios-red/15",
        link: "text-ios-blue underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-4 gap-2",
        sm: "h-8 px-3 text-xs gap-1.5",
        lg: "h-11 px-6 gap-2",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

function Button({
  className,
  variant = "default",
  size = "default",
  ...props
}: React.ComponentProps<"button"> & VariantProps<typeof buttonVariants>) {
  return (
    <button
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  )
}

export { Button, buttonVariants }
