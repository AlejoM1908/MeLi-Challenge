interface InputProps {
    handle_change: React.ChangeEventHandler
    value: string
    label_text: string
    label_for: string
    id: string
    type: string
    name: string
    is_required: boolean
    placeholder: string
    className?: string
}

export function Input({
    handle_change,
    value,
    label_text,
    label_for,
    id,
    type,
    name,
    is_required,
    placeholder,
    className,
}: InputProps): JSX.Element {
    return (
        <div className="my-5">
            <label htmlFor={label_for} className="sr-only">
                {label_text}
            </label>
            <input
                onChange={handle_change}
                value={value}
                type={type}
                id={id}
                name={name}
                required={is_required}
                placeholder={placeholder}
                className={`rounded-md appearance-none relative block w-full px-3 py-2 border-2 border-border-light placeholder-sh-dark text-tx-light dark:border-border-dark focus:outline-none focus:border-bu-color focus:dark:border-bu-color focus:z-10 sm:text-sm ${className}`}
            />
        </div>
    )
}