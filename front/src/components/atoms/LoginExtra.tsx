export function LoginExtra(): JSX.Element {
  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center">
        <input
          id="remember_me"
          name="remember_me"
          type="checkbox"
          className="h-4 w-4 text-bu-color focus:ring-bu-color border-gray-300 rounded"
        />
        <label
          htmlFor="remember_me"
          className="ml-2 block text-sm text-tx-light dark:text-tx-dark"
        >
          Remember me
        </label>

        <a
          href="#"
          className="ml-2 text-sm text-bu-color hover:underline dark:text-bu-color"
        >
          Forgot your password?
        </a>
      </div>
    </div>
  );
}
