import { gsap } from "gsap";

// Called inside the motion media context, so reduced motion restores static HTML.
export function initializeRoles(signal: AbortSignal) {
  const display = document.querySelector<HTMLElement>(".role-display");
  const first = display?.querySelector<HTMLElement>(".role-first");
  const second = display?.querySelector<HTMLElement>(".role-second");
  const firstDot = display?.querySelector<HTMLElement>('[data-line="first"]');
  const secondDot = display?.querySelector<HTMLElement>('[data-line="second"]');
  if (!display || !first || !second || !firstDot || !secondDot) return () => {};

  const roles = [
    "Product Engineer",
    "Full Stack Engineer",
    "Frontend Engineer",
  ];
  const render = (role: string, count: number) => {
    const split = role.lastIndexOf(" ");
    first.textContent = role.slice(0, Math.min(count, split));
    second.textContent = count > split ? role.slice(split + 1, count) : "";
    firstDot.hidden = count > split;
    secondDot.hidden = count <= split;
  };
  let inView = false;
  const cursor = { count: roles[0].length };
  const rotation = gsap.timeline({ repeat: -1, paused: true });
  for (let index = 0; index < roles.length; index++) {
    const current = roles[index];
    const next = roles[(index + 1) % roles.length];
    rotation
      .to({}, { duration: 3.2 })
      .fromTo(
        cursor,
        { count: current.length },
        {
          count: 0,
          duration: current.length * 0.045,
          ease: "none",
          snap: { count: 1 },
          immediateRender: false,
          onUpdate: () => render(current, cursor.count),
        },
      )
      .to({}, { duration: 0.2 })
      .fromTo(
        cursor,
        { count: 0 },
        {
          count: next.length,
          duration: next.length * 0.09,
          ease: "none",
          snap: { count: 1 },
          immediateRender: false,
          onUpdate: () => render(next, cursor.count),
        },
      );
  }
  const blink = gsap.to(display.querySelectorAll(".role-dot"), {
    opacity: 0.15,
    duration: 0.7,
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut",
    paused: true,
  });
  const sync = () => {
    const playing = inView && !document.hidden;
    rotation.paused(!playing);
    blink.paused(!playing);
  };
  document.addEventListener("visibilitychange", sync, { signal });
  const observer = new IntersectionObserver(([entry]) => {
    inView = entry.isIntersecting;
    sync();
  });
  observer.observe(display);

  return () => {
    observer.disconnect();
    rotation.kill();
    blink.kill();
    render(roles[0], roles[0].length);
  };
}
