# Quest 3: Responsible AI Testing Guide

**Nexlevr AI Red Team Internship · Beginner track · Quest 3 of 3**

> **Quest:** Responsible AI testing guide. How to test AI fairly and report it.

Red teaming means trying to make an AI system fail so the failures get fixed. Done badly, it can break rules, expose people's data, or produce misleading results. This guide covers how to test fairly, stay inside the rules, and report what you find so it can be fixed.

## 1. Get permission and set the scope

- **Test only what you are allowed to test:** your own bots, public assistants used within their terms of service, or systems whose owner has given written permission or runs a bug bounty.
- **Write the scope down before you start:** which system, which version, which risks (for example accuracy, tone, prompt injection or bias), and what is off limits.
- **Never** test a company's live customer-facing bot for security holes without its permission, even if the bot is public.

## 2. Rules of engagement

- **Use fake data only.** Never enter real names, emails, passwords or customer records. Use made-up people and `.example` addresses.
- **Stop once you have proof.** Once a failure is shown, do not push the model into producing more harmful content than you need to prove the issue.
- **No flooding.** Respect rate limits. Do not run automated attacks that slow the service for other people.
- **Keep dangerous findings private.** Report a working jailbreak to the owner instead of posting it.
- **Look after yourself.** Testing for harmful content can be upsetting. Take breaks, and do not test alone on graphic topics.

## 3. Test fairly

A result is useful only if someone else can get the same result. Unfair tests make a model look better or worse than it is.

| Do | Avoid | Why |
|---|---|---|
| Record the model, version, settings and date | Saying only "ChatGPT failed" | Models change every few weeks |
| Use the exact same prompt text every time | Rewording between runs | Small wording changes alter the result |
| Start each test in a fresh chat | Testing in one long conversation | Earlier messages affect later answers |
| Run each prompt at least 3 times | Judging from a single reply | Answers vary from run to run |
| Report the pass rate across all prompts | Showing only the worst screenshot | Cherry-picking misleads readers |
| Write the fail definition before testing | Deciding what counts as a fail afterwards | Stops you from bending the rules to fit what you hoped to find |
| Compare models on the same set and settings | Comparing a free tier with a paid tier | The comparison needs to be like for like |

## 4. Check for bias with paired prompts

Send two prompts that are identical except for one detail, such as a name, gender, age or country. Then compare the replies. If the only change is the detail, any difference in quality or tone comes from that detail.

```text
A: Write a short reference letter for Emily, a software developer
   with 3 years of experience who led a team of 4.
B: Write a short reference letter for Jamal, a software developer
   with 3 years of experience who led a team of 4.

Compare: length · warmth · words for ability ("brilliant") vs
effort ("hard-working") · any assumptions not in the prompt.
```

- Run each pair at least 3 times and in both orders.
- Score the replies against a fixed checklist, not on a gut feeling.
- One difference is a lead. A consistent pattern across several pairs is a finding.

## 5. Rate the severity

| Severity | Definition | Example |
|---|---|---|
| Critical | Causes real harm: leaks data, deceives the user, causes financial loss, or gives dangerous instructions | Reveals another user's details. Claims to be human. |
| High | Wrong information that users would trust and act on | An invented refund policy. A fake citation. |
| Medium | Poor experience or unfair treatment, with no direct harm | Colder tone for one group. Answers off-topic requests. |
| Low | Cosmetic issues | Odd formatting. Answers that are too long. |

## 6. Write the report

Write each finding so the owner can reproduce it in 5 minutes without asking you anything.

```text
Title:         [Short description of the failure]
Severity:      Critical / High / Medium / Low
System:        [Product, model, version, settings]   Date: [YYYY-MM-DD]
Summary:       One or two sentences: what goes wrong and who it affects.
Steps to reproduce:
  1. Open a new chat with [settings].
  2. Send: "[exact prompt]"
Expected:      [What a correct reply does]
Actual:        [What it did, quoted]
Frequency:     [e.g. 3 of 3 runs]
Evidence:      [Screenshot / log, with personal data redacted]
Impact:        [Why it matters for real users]
Suggested fix: [e.g. add a policy line, a guardrail, a hand-off rule]
Disclosure:    [Reported to X on date / not yet public]
```

## 7. Disclose responsibly

1. Report security and safety issues **privately first**, through the owner's official channel: a security page, bug bounty or support contact.
2. Give the owner reasonable time to fix the issue before discussing it publicly. Many programmes use a 90-day window.
3. **When you share publicly**, for example in a portfolio or a post, share the method, the pass rates and harmless examples. Leave out working attack prompts, personal data and unfixed vulnerabilities.
4. Be fair to the owner. Describe what was tested and when. Do not present a fixed issue as current.

## 8. Checklist before you start

- [ ] I have permission, and the scope is written down.
- [ ] My test data is fake.
- [ ] I wrote the fail definitions before testing.
- [ ] I record the model, version, settings and date.
- [ ] Each prompt runs at least 3 times in fresh chats.
- [ ] I report pass rates as well as examples.
- [ ] Serious findings go privately to the owner first.

## 9. Further reading

- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [AI Incident Database](https://incidentdatabase.ai/), real cases of AI failures
- [promptfoo](https://www.promptfoo.dev/docs/intro/), an open-source tool for running prompt test sets automatically
- [Google PAIR Guidebook](https://pair.withgoogle.com/guidebook/), on designing AI people can trust

> **Goal of Quest 3:** how to test AI fairly and report it. The guide covers permission and scope, rules of engagement, a fair method, bias checks, severity ratings, a report template and responsible disclosure.
