import { ae as ordered_colors } from './index.b9670dcf.js';

const get_next_color = (index) => {
  return ordered_colors[index % ordered_colors.length];
};

export { get_next_color as g };
