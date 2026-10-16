// Release catalog for gracechase.com.
// Streaming links were checked against Apple Music, Amazon Music,
// YouTube Music, and Spotify in October 2026. Spotify album ids for
// the three newest releases were confirmed by Moses.

export const PLATFORM_STORAGE_KEY = 'gracechase-platform'

export const platforms = [
  {
    id: 'spotify',
    label: 'Spotify',
    icon: 'images/link-icons/Alt Streaming Service Icons/Spotify_Primary_Logo_RGB_Green.png?v=2',
  },
  {
    id: 'appleMusic',
    label: 'Apple Music',
    icon: 'images/link-icons/Alt Streaming Service Icons/music.cce3eb3f.svg',
  },
  {
    id: 'youtubeMusic',
    label: 'YouTube Music',
    icon: 'images/link-icons/YT_music_logo.png',
  },
  {
    id: 'amazonMusic',
    label: 'Amazon Music',
    icon: 'images/link-icons/amazon_music_logo.png',
  },
]

// Holiday art stays up through December 31, 2026, local time.
const HOLIDAY_ENDS = new Date(2027, 0, 1)

export function isHolidaySeason(now = new Date()) {
  return now < HOLIDAY_ENDS
}

export const holidayGallery = [
  { src: 'images/holiday/gallery-01.jpg', alt: 'Gracechase gathered in the snow with a sled and gifts' },
  { src: 'images/holiday/gallery-02.jpg', alt: 'Gracechase at a snowy Christmas market, holding a wreath' },
  { src: 'images/holiday/gallery-03.jpg', alt: 'Gracechase decorating a Christmas tree on a frozen mountain lake' },
  { src: 'images/holiday/gallery-04.jpg', alt: 'Gracechase on a cabin porch beside a lit Christmas tree' },
]

export const holidayImages = {
  banner: 'images/holiday/banner.jpg',
  bannerAlt: 'Gracechase riding a Christmas train through the snow',
  fireside: 'images/holiday/fireside.jpg',
  firesideAlt: 'Gracechase by the fireplace with a Christmas tree',
}

export const releases = [
  {
    slug: 'christmas-window',
    title: 'Christmas Window',
    type: 'album',
    holiday: true,
    releaseDate: '2026-10-11',
    year: 2026,
    trackCount: 9,
    blurb: 'Nine new Christmas songs, out now.',
    cover: 'images/album-covers/christmas-window.jpg',
    links: {
      appleMusic: 'https://music.apple.com/us/album/christmas-window/6821818870',
      amazonMusic: 'https://music.amazon.com/albums/B0HMPRC746',
      youtubeMusic: 'https://music.youtube.com/playlist?list=OLAK5uy_miNnQtv-2ZfEPOhfN1-R69KSxJYF9FVOo',
      spotify: 'https://open.spotify.com/album/3U3ytobaQ2fQWxnKkduTfu',
    },
    tracks: [
      'I Still Care About Your Christmas',
      'Made With Love',
      'Window',
      'Christmas Miracle',
      'Too Old For Christmas',
      'Behold the King',
      'All I Need (Christmas Version)',
      'One Last Christmas in Colorado',
      "We'll Make Our Own Christmas Lights",
    ],
  },
  {
    slug: 'this-is-how-you-christmas',
    title: 'This Is How You Christmas',
    type: 'single',
    holiday: true,
    releaseDate: '2026-10-11',
    year: 2026,
    trackCount: 1,
    blurb: 'The new Christmas single.',
    cover: 'images/album-covers/this-is-how-you-christmas.jpg',
    links: {
      appleMusic: 'https://music.apple.com/us/album/this-is-how-you-christmas-single/6821836999',
      amazonMusic: 'https://music.amazon.com/albums/B0HMPL4BWV',
      youtubeMusic: 'https://music.youtube.com/playlist?list=OLAK5uy_kEQsUSMv4Er8PY8IJDkxHVkzCKYKX8D6M',
      spotify: 'https://open.spotify.com/album/1yrPKeMwvW5igfIhowRYua',
    },
    tracks: ['This Is How You Christmas'],
  },
  {
    slug: 'america-to-me',
    title: 'America To Me',
    type: 'single',
    holiday: false,
    releaseDate: '2026-06-27',
    year: 2026,
    trackCount: 1,
    blurb: 'A single for home.',
    cover: 'images/album-covers/america-to-me.jpg',
    links: {
      appleMusic: 'https://music.apple.com/us/album/america-to-me-single/6785311089',
      amazonMusic: 'https://music.amazon.com/albums/B0H6T87GGD',
      youtubeMusic: 'https://music.youtube.com/playlist?list=OLAK5uy_leos1WpdDQjcb2i7CWwmTpcM3mydA65Lc',
      spotify: 'https://open.spotify.com/album/2e269MOQgfIVSCjF2qpGwX',
    },
    tracks: ['America To Me'],
  },
  {
    slug: 'unserious',
    title: 'Unserious',
    type: 'album',
    holiday: false,
    releaseDate: '2026-05-17',
    year: 2026,
    trackCount: 11,
    blurb: 'Eleven songs with a lighter step.',
    cover: 'images/album-covers/unserious.jpg',
    links: {
      spotify: 'https://open.spotify.com/album/546ErSciiwGNrta0anT49e',
      appleMusic: 'https://music.apple.com/us/album/unserious/6770580267',
      youtubeMusic: 'https://music.youtube.com/playlist?list=OLAK5uy_mplVYVTcc1J1C1rijb5aPRPe6XKwNiByE',
      amazonMusic: 'https://music.amazon.com/albums/B0H24PCJWF',
    },
    tracks: [
      'Barista',
      'Fairytales',
      'Home Run',
      'I Call It Art',
      'Seven More Days',
      'On My Way Home',
      'Look Both Ways',
      'Factory Reset',
      'WAKE UP!',
      'I Just Needed a Hug',
      'Another Cup of Coffee',
    ],
  },
  {
    slug: 'up-to-you',
    title: 'Up to You',
    type: 'album',
    holiday: false,
    releaseDate: '2026-05-16',
    year: 2026,
    trackCount: 12,
    blurb: 'Twelve songs about choosing what comes next.',
    cover: 'images/album-covers/up-to-you.jpg',
    links: {
      spotify: 'https://open.spotify.com/album/5ApS7bjPkKj0ybq8Tg6kj0',
      appleMusic: 'https://music.apple.com/us/album/up-to-you/6772195339',
      youtubeMusic: 'https://music.youtube.com/playlist?list=OLAK5uy_n9j9g4aVdd2SYvY9xnC96ByGgp8bH5KMQ',
      amazonMusic: 'https://music.amazon.com/albums/B0H23599KK',
    },
    tracks: [
      'A Door God Opened',
      'Redefining',
      'My King',
      'Wait',
      'Calling Me',
      'Left for Dead',
      'Maybe Now (Like Right Now)',
      'You Are (Awesome)',
      'Please',
      'Picked up the Pieces',
      'Up to You',
      'You Light Up My Soul',
    ],
  },
  {
    slug: 'set-me-free',
    title: 'Set Me Free',
    type: 'album',
    holiday: false,
    releaseDate: '2026-02-16',
    year: 2026,
    trackCount: 13,
    blurb: 'Thirteen songs about being set free.',
    cover: 'images/album-covers/set-me-free.jpg',
    links: {
      spotify: 'https://open.spotify.com/album/17n7rXpMd7OqsIkfjQQDDR',
      appleMusic: 'https://music.apple.com/us/album/set-me-free/1878887745',
      youtubeMusic: 'https://music.youtube.com/playlist?list=OLAK5uy_kO4ztJC1BtAXZTzuvXEh44m22aGglsgKo',
      amazonMusic: 'https://music.amazon.com/albums/B0GNPDJP9H',
    },
    tracks: [
      'Set Me Free (Free Indeed)',
      'Mercy Is',
      'Right Place, Right Time',
      'Even More Than I Do',
      'Give Me a Heart (For the Lost)',
      'Unshakeable',
      'Upside-Down',
      'Your Voice (Psalm 29)',
      'Change Me',
      'Heart',
      'My Soul is Safe',
      'Right Now',
      'Angels',
    ],
  },
  {
    slug: 'even-better-christmas',
    title: 'Even Better Christmas',
    type: 'album',
    holiday: true,
    releaseDate: '2025-11-01',
    year: 2025,
    trackCount: 15,
    blurb: "Last year's Christmas album.",
    cover: 'images/album-covers/even-better-christmas.jpg?v=3',
    links: {
      spotify: 'https://open.spotify.com/album/0FDPRyIXg50LXOdgH8g65b',
      appleMusic: 'https://music.apple.com/us/album/even-better-christmas/1847634777',
      youtubeMusic: 'https://music.youtube.com/playlist?list=OLAK5uy_n_fdOT3WVxXeKfjr-h2arrYbk623z3VRU',
      amazonMusic: 'https://music.amazon.com/albums/B0FWZ9VRCF',
    },
    tracks: [
      'Even Better Christmas',
      'To Hear the Angels Sing',
      "Joy! Everything's Alright!",
      'Christmas Party (All the Way)',
      'Hark! The Herald Angels Sing',
      'Christmas Again',
      'Keep Christmas Alive',
      'Let it be Christmas (All Year)',
      'The Long Road Home',
      'Venite Adoremus Dominum (O Come, Let Us Adore The Lord)',
      'Let My Heart Find Christmas',
      'Angels We Have Heard on High',
      'The Same Stars (Is it Snowing)',
      'Jingle Bells',
      'Sound of Christmas',
    ],
  },
  {
    slug: 'your-majesty',
    title: 'Your Majesty',
    type: 'album',
    holiday: false,
    releaseDate: '2025-09-20',
    year: 2025,
    trackCount: 14,
    blurb: 'Fourteen songs of worship.',
    cover: 'images/album-covers/your-majesty.jpg?v=3',
    links: {
      spotify: 'https://open.spotify.com/album/0eRcQ32hkwgvSvfPPPOOhu',
      appleMusic: 'https://music.apple.com/us/album/your-majesty/1841459632',
      youtubeMusic: 'https://music.youtube.com/playlist?list=OLAK5uy_kVbhrim-szUB-OAs0nCayOWOijpXukKCA',
      amazonMusic: 'https://music.amazon.com/albums/B0FRYSGZ4C',
    },
    tracks: [
      'Your Majesty',
      'In the Light',
      'Awesome, Wonderful God',
      'Follow After You',
      'Number of the Stars',
      'Lord Take My Guitar',
      'Paid in Full',
      'Not a Day',
      'The Brighter the Stars Shine',
      "As Long As There's Life",
      'Without Me',
      'Waves Are Rising',
      'All I Need',
      'Shooting Star',
    ],
  },
  {
    slug: 'im-still-your-love',
    title: "I'm Still Your Love",
    type: 'single',
    holiday: false,
    releaseDate: '2025-08-24',
    year: 2025,
    trackCount: 1,
    blurb: 'A single.',
    cover: 'images/album-covers/im-still-your-love.jpg',
    links: {
      spotify: 'https://open.spotify.com/album/5Tt1sGIoAnpzRHY3abDqz4',
      appleMusic: 'https://music.apple.com/us/album/im-still-your-love-single/1835662171',
      youtubeMusic: 'https://music.youtube.com/watch?v=QoaeKUHDJM8',
      amazonMusic: 'https://music.amazon.com/albums/B0FNLZ7CJ4',
    },
    tracks: ["I'm Still Your Love"],
  },
]

export function getRelease(slug) {
  return releases.find((release) => release.slug === slug) || null
}

export function spotifyAlbumId(release) {
  const link = release?.links?.spotify
  if (!link) return null
  const match = link.match(/album\/([a-zA-Z0-9]+)/)
  return match ? match[1] : null
}

export function availablePlatforms(release) {
  return platforms.filter((platform) => Boolean(release.links?.[platform.id]))
}

// During the holidays the hero is Christmas Window, with the new single
// and last year's album beside it. After that, the most recent
// non-Christmas albums take the same spots.
export function getSpotlight(now = new Date()) {
  if (isHolidaySeason(now)) {
    return {
      holiday: true,
      hero: getRelease('christmas-window'),
      also: [getRelease('this-is-how-you-christmas'), getRelease('even-better-christmas')],
    }
  }
  const albums = releases
    .filter((release) => release.type === 'album' && !release.holiday)
    .sort((a, b) => b.releaseDate.localeCompare(a.releaseDate))
  return {
    holiday: false,
    hero: albums[0],
    also: albums.slice(1, 3),
  }
}
