import { MeLiLogo } from "../../assets/icons/meli";

interface LoginHeaderProps {
    heading: string
    subheading?: string
    link_text?: string
    link_url?: string
}

export function LoginHeader({ heading, subheading, link_text, link_url = '/' }: LoginHeaderProps) : JSX.Element {
    return(
        <div className="mb-10">
            <div className="flex justify-center">
                <MeLiLogo className="w-64 h-auto max-w-full" />
            </div>
            <h2 className="mt-6 text-center text-3xl font-extrabold text-tx-light dark:text-tx-dark">
                {heading}
            </h2>
            <p className="mt-2 text-center text-sm text-tx-light dark:text-tx-dark">
                {subheading}
                {' '}
                <a href={link_url} className="font-medium text-bu-color hover:text-bu-color-hover">
                    {link_text}
                </a>
            </p>
        </div>
    );
}