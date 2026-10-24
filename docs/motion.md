# Motion and icons

`src/scripts/motion.ts` owns GSAP, ScrollTrigger and the single Lenis scroll instance. It runs only when reduced motion is not requested. Touch retains native scrolling. Offscreen cards reveal once; Impact cards use a 120ms stagger. The portrait is static.

`src/scripts/roles.ts` types Product Engineer, Full Stack Engineer and Frontend Engineer in a fixed two-line slot. Complete roles stay visible for 3.2 seconds; typing uses 90ms per character and deletion 45ms. The dot pulses every 1.4 seconds. Rotation pauses outside the viewport and in background tabs. Screen readers receive a stable label containing all three roles.

Without JavaScript or with reduced motion enabled, the page shows Product Engineer and all content remains readable. Media-query changes, pagehide, bfcache restoration and hot reload clean up listeners, observers, timelines and the scroll engine. Scroll measurements refresh after fonts, images, details and layout changes.

`src/styles/motion-design.css` loads after the shared responsive stylesheet and contains role, icon, screen and print rules. Buttons and their arrows move together; keyboard focus stays visible. Print uses a static Product Engineer heading.

## Assets

The original portrait is supplied by Andrii Deisan. Astro generates responsive WebP images; its CSS color treatment does not modify the source image.

Interface arrows use Solar by 480 Design through `@iconify-json/solar`, rendered as inline SVG by `Icon.astro`. Sizes and colors are adapted for buttons, inline links, metrics and the course disclosure. Metric data and accessible labels preserve the original wording. Attribution and the CC BY 4.0 license link are in `public/third-party-notices.txt`.
