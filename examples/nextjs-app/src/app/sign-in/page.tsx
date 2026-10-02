import { SignInForm } from "@/components/sign-in-form";

export default function SignInPage() {
  return (
    <>
      <h1>Sign in locally</h1>
      <p>
        Use a synthetic username (alex, sam, viewer or outsider) and the
        generated password in your private disposable runtime.json. No external
        SSO is tested.
      </p>
      <SignInForm />
    </>
  );
}
