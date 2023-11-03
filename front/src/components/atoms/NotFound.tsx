import { ThemeToggle } from './ThemeToggle'

interface NotFoundProps {
  homePath: string
  className?: string
}

export function NotFound({ homePath, className }: NotFoundProps): JSX.Element {
  return (
    <div
      className={`grid h-screen px-4 bg-light dark:bg-dark items-center ${className}`}
    >
      <div className="text-center">
        <div className="mb-14">
          <ThemeToggle />
        </div>
        <h1 className="font-black text-tx-light dark:text-tx-dark text-9xl">
          404
        </h1>

        <p className="text-2xl font-bold tracking-tight text-th-accent sm:text-4xl">
          Uh-oh!
        </p>

        <p className="mt-4 text-tx-light dark:text-tx-dark">
          We can't find that page.
        </p>

        <a
          href={homePath}
          className="inline-block px-5 py-3 mt-6 text-sm font-medium text-white bg-th-accent rounded hover:bg-th-muted focus:outline-none focus:ring"
        >
          {' '}
          Go Back Home
        </a>
      </div>
    </div>
  )
}
