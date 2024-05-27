/// <reference path="../.astro/types.d.ts" />
/// <reference types="astro/client" />

interface TextProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  color?: 'white' | 'black' | 'blue';
  uppercase?: boolean;
  customClass?: string;
}
