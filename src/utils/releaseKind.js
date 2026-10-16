export function releaseKind(release) {
  return release.type === 'single' ? 'Single' : 'Album';
}
