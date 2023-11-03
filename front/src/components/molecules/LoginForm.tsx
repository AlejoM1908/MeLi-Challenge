import { LoginHeader } from "../atoms/LoginHeader";
import { LoginExtra } from "../atoms/LoginExtra";
import { useState } from "react";
import { Input } from "../atoms/Input";
import { LOGIN_INPUTS } from "../../utils/constants/loginFields";

let field_states: { [key: string]: string } = {};

LOGIN_INPUTS.forEach((input) => {
  field_states[input.id] = "";
});

interface LoginFormProps {
  action?: "submit" | "button" | "reset" | undefined;
  button_text: string;
  endpoint?: string;
}

export function LoginForm({ action = "submit", button_text, endpoint }: LoginFormProps): JSX.Element {
  const [login_state, setLoginState] = useState(field_states);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setLoginState({
      ...login_state,
      [event.target.id]: event.target.value,
    });
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    AuthUser();
    window.location.href = "/";
  };

  const AuthUser = async () => {
    console.log("i'm working")
    const response = await fetch(process.env.API_URL + '/v1.1/login', {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: login_state.email,
        password: login_state.password,
      }),
    });

    if (!response.ok) {
      throw new Error(response.statusText);
    }

    const data = await response.json();
    localStorage.setItem("jwt", data.jwt);
    localStorage.setItem("refresh", data.refresh);
  };

  return (
    <>
      <LoginHeader heading="Sign in to your account" />
      <form className="mt-8 space-y-6">
        <div className="-space-y-px">
          {LOGIN_INPUTS.map((input) => (
            <Input
              key={input.id}
              handle_change={handleChange}
              value={login_state[input.id]}
              label_text={input.label_text}
              label_for={input.label_for}
              id={input.id}
              type={input.type}
              name={input.name}
              is_required={input.required}
              placeholder={input.placeholder}
            ></Input>
          ))}
        </div>
        <button
          type={action}
          onClick={(event: React.FormEvent<HTMLFormElement>) => handleSubmit(event)}
          className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-bu-color hover:bg-bu-hover focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-bu-hover"
        >
          {button_text}
        </button>
      </form>
    </>
  );
}
