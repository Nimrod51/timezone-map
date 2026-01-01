/**
 * Color schemes for timezone visualization
 * Each scheme defines how timezones are colored based on work_hours_CET
 */

const COLOR_SCHEMES = {
  'high-contrast': {
    name: 'High Contrast',
    description: 'Distinct colors for maximum differentiation',
    type: 'match',
    colors: [
      'match',
      ['to-number', ['slice', ['get', 'work_hours_CET'], 0, 2]],
      0, '#e74c3c',    // red (midnight)
      1, '#3498db',    // blue
      2, '#f39c12',    // orange
      3, '#9b59b6',    // purple
      4, '#1abc9c',    // turquoise
      5, '#e67e22',    // carrot orange
      6, '#2ecc71',    // green
      7, '#c0392b',    // dark red
      8, '#16a085',    // dark turquoise
      9, '#f1c40f',    // yellow (9am - CET reference)
      10, '#8e44ad',   // dark purple
      11, '#27ae60',   // dark green
      12, '#e84393',   // pink
      13, '#0984e3',   // bright blue
      14, '#d63031',   // bright red
      15, '#00b894',   // mint
      16, '#fdcb6e',   // light orange
      17, '#6c5ce7',   // indigo
      18, '#00cec9',   // cyan
      19, '#ff7675',   // light red
      20, '#74b9ff',   // light blue
      21, '#a29bfe',   // lavender
      22, '#fd79a8',   // light pink
      23, '#55efc4',   // aqua
      '#888888'        // fallback gray
    ]
  },

  'gradient-cool': {
    name: 'Cool Gradient',
    description: 'Smooth cyan-purple gradient (original)',
    type: 'interpolate',
    colors: [
      'interpolate',
      ['linear'],
      ['to-number', ['slice', ['get', 'work_hours_CET'], 0, 2]],
      0, '#d32f2f',    // red (midnight)
      3, '#e91e63',    // pink
      6, '#9c27b0',    // purple
      9, '#673ab7',    // deep purple (9am - CET reference)
      12, '#3f51b5',   // indigo (noon)
      15, '#2196f3',   // blue
      18, '#00bcd4',   // cyan (6pm)
      21, '#009688',   // teal (9pm)
      22, '#ff5722'    // deep orange (10pm)
    ]
  },

  'warm-cool': {
    name: 'Warm/Cool',
    description: 'Warm colors (morning) to cool colors (evening)',
    type: 'interpolate',
    colors: [
      'interpolate',
      ['linear'],
      ['to-number', ['slice', ['get', 'work_hours_CET'], 0, 2]],
      0, '#1a1a2e',    // midnight blue
      3, '#ff6b6b',    // coral red (early morning)
      6, '#feca57',    // yellow (sunrise)
      9, '#48dbfb',    // sky blue (morning - CET reference)
      12, '#0abde3',   // ocean blue (noon)
      15, '#5f27cd',   // purple (afternoon)
      18, '#341f97',   // deep purple (evening)
      21, '#222f3e',   // dark blue (night)
      23, '#1a1a2e'    // back to midnight
    ]
  },

  'earth-tones': {
    name: 'Earth Tones',
    description: 'Natural colors inspired by landscapes',
    type: 'interpolate',
    colors: [
      'interpolate',
      ['linear'],
      ['to-number', ['slice', ['get', 'work_hours_CET'], 0, 2]],
      0, '#2d3436',    // dark gray (midnight)
      3, '#636e72',    // gray
      6, '#a29bfe',    // lavender (dawn)
      9, '#ffeaa7',    // cream (morning - CET reference)
      12, '#fdcb6e',   // golden (noon)
      15, '#e17055',   // terracotta (afternoon)
      18, '#d63031',   // brick red (evening)
      21, '#6c5ce7',   // purple (twilight)
      23, '#2d3436'    // back to dark
    ]
  },

  'rainbow': {
    name: 'Rainbow',
    description: 'Full spectrum across 24 hours',
    type: 'interpolate',
    colors: [
      'interpolate',
      ['linear'],
      ['to-number', ['slice', ['get', 'work_hours_CET'], 0, 2]],
      0, '#ff0000',    // red
      4, '#ff7f00',    // orange
      8, '#ffff00',    // yellow
      9, '#7fff00',    // chartreuse (CET reference)
      12, '#00ff00',   // green
      16, '#00ff7f',   // spring green
      18, '#00ffff',   // cyan
      20, '#0000ff',   // blue
      22, '#8b00ff',   // violet
      23, '#ff0000'    // back to red
    ]
  },

  'monochrome-blue': {
    name: 'Monochrome Blue',
    description: 'Single hue with varying intensity',
    type: 'interpolate',
    colors: [
      'interpolate',
      ['linear'],
      ['to-number', ['slice', ['get', 'work_hours_CET'], 0, 2]],
      0, '#0a1929',    // very dark blue (midnight)
      6, '#1e3a5f',    // dark blue
      9, '#2563eb',    // medium blue (CET reference)
      12, '#3b82f6',   // bright blue (noon)
      18, '#60a5fa',   // light blue
      23, '#0a1929'    // back to very dark
    ]
  }
};

// Get color expression for a given scheme
function getColorExpression(schemeName) {
  const scheme = COLOR_SCHEMES[schemeName];
  return scheme ? scheme.colors : COLOR_SCHEMES['high-contrast'].colors;
}

// Get all scheme names for UI
function getSchemeNames() {
  return Object.keys(COLOR_SCHEMES);
}

// Get scheme metadata
function getSchemeInfo(schemeName) {
  return COLOR_SCHEMES[schemeName] || COLOR_SCHEMES['high-contrast'];
}
