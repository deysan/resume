import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Lenis from "lenis";
import "lenis/dist/lenis.css";
import { initializeRoles } from "./roles";

gsap.registerPlugin(ScrollTrigger);

let dispose: (() => void) | undefined;

function initializeMotion() {
  dispose?.();
  const media = gsap.matchMedia();
  media.add("(prefers-reduced-motion: no-preference)", () => {
    const listeners = new AbortController();
    const { signal } = listeners;
    let alive = true;
    const disposeRoles = initializeRoles(signal);

    // One scroll engine and one shared frame clock. Touch keeps native inertia.
    const lenis = new Lenis({
      smoothWheel: true,
      syncTouch: false,
      lerp: 0.12,
    });
    lenis.on("scroll", ScrollTrigger.update);
    const tick = (time: number) => lenis.raf(time * 1000);
    gsap.ticker.add(tick);
    gsap.ticker.lagSmoothing(0);

    // Keep the compact hero fully readable throughout its entrance.
    const intro = gsap.timeline({
      defaults: { ease: "power3.out", duration: 0.85 },
    });
    intro
      .from(".hero-copy", { y: 12 }, 0)
      .from(".hero-actions", { y: 12 }, 0.16);

    // Prepare only offscreen blocks, before they enter the viewport. No nested
    // heading tweens or visible → hidden jumps when the trigger starts.
    document
      .querySelectorAll<HTMLElement>(
        ".profile, .impact-card, .job, .sidebar > section, .contact",
      )
      .forEach((block) => {
        if (block.getBoundingClientRect().top <= window.innerHeight) return;
        gsap.fromTo(
          block,
          { y: 38, opacity: 0.12 },
          {
            y: 0,
            opacity: 1,
            duration: 1,
            delay: block.matches(".impact-card")
              ? Array.from(block.parentElement!.children).indexOf(block) * 0.12
              : 0,
            ease: "power3.out",
            clearProps: "transform,opacity",
            scrollTrigger: { trigger: block, start: "top 92%", once: true },
          },
        );
      });

    gsap.to(".reading-progress", {
      scaleX: 1,
      ease: "none",
      scrollTrigger: { start: 0, end: "max", scrub: true },
    });

    // Keep real anchors, URL hashes and keyboard focus; modified clicks stay native.
    document.addEventListener(
      "click",
      (event) => {
        if (
          event.defaultPrevented ||
          event.button !== 0 ||
          event.metaKey ||
          event.ctrlKey ||
          event.shiftKey ||
          event.altKey
        )
          return;
        const link = (event.target as Element).closest<HTMLAnchorElement>(
          'a[href^="#"]',
        );
        if (!link || link.target || link.hasAttribute("download")) return;
        const id = link.hash.slice(1);
        const target = document.getElementById(id);
        if (!target) return;
        event.preventDefault();
        lenis.scrollTo(target, {
          onComplete: () => {
            history.pushState(null, "", link.hash);
            const hadTabindex = target.hasAttribute("tabindex");
            if (!hadTabindex) target.setAttribute("tabindex", "-1");
            target.focus({ preventScroll: true });
            if (!hadTabindex)
              target.addEventListener(
                "blur",
                () => target.removeAttribute("tabindex"),
                { once: true, signal },
              );
          },
        });
      },
      { signal },
    );

    window.addEventListener(
      "hashchange",
      () => {
        const target = document.getElementById(
          decodeURIComponent(location.hash.slice(1)),
        );
        if (target) lenis.scrollTo(target, { immediate: true, force: true });
      },
      { signal },
    );

    let timer: ReturnType<typeof setTimeout>;
    const refresh = () => {
      clearTimeout(timer);
      timer = setTimeout(() => {
        if (alive) {
          lenis.resize();
          ScrollTrigger.refresh();
        }
      }, 80);
    };
    const observer = new ResizeObserver(refresh);
    const main = document.querySelector("main");
    if (main) observer.observe(main);
    document
      .querySelectorAll("details")
      .forEach((details) =>
        details.addEventListener("toggle", refresh, { signal }),
      );
    document.fonts.ready.then(() => {
      if (alive) refresh();
    });
    document.querySelectorAll("img").forEach((img) => {
      if (!img.complete) img.addEventListener("load", refresh, { signal });
    });

    const pause = () => {
      intro.pause();
      lenis.stop();
      gsap.ticker.remove(tick);
    };
    const resume = () => {
      if (document.hidden) return;
      intro.resume();
      lenis.start();
      gsap.ticker.add(tick);
      refresh();
    };
    document.addEventListener(
      "visibilitychange",
      () => (document.hidden ? pause() : resume()),
      { signal },
    );
    window.addEventListener(
      "blur",
      () => {
        intro.progress(1);
      },
      { signal },
    );
    window.addEventListener("focus", resume, { signal });

    return () => {
      alive = false;
      clearTimeout(timer);
      listeners.abort();
      observer.disconnect();
      gsap.ticker.remove(tick);
      lenis.destroy();
      disposeRoles();
    };
  });
  dispose = () => media.revert();
}

initializeMotion();
const onPageHide = () => dispose?.();
const onPageShow = (event: PageTransitionEvent) => {
  if (event.persisted) initializeMotion();
};
window.addEventListener("pagehide", onPageHide);
window.addEventListener("pageshow", onPageShow);

if (import.meta.hot)
  import.meta.hot.dispose(() => {
    dispose?.();
    window.removeEventListener("pagehide", onPageHide);
    window.removeEventListener("pageshow", onPageShow);
  });
