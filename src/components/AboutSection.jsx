export default function AboutSection() {
  return (
    <section className="gc-about" id="about" aria-labelledby="gc-about-title">
      <div className="gc-about__inner">
        <h2 id="gc-about-title" className="gc-eyebrow">About Gracechase</h2>
        <p className="gc-about__tagline">Grace has been chasing you. Maybe it's time to stop running.</p>
        <div className="gc-about__cols">
          <div>
            <h3 className="gc-about__h3">Our Story</h3>
            <p>
              Hey there! We are Gracechase. We're an innovative music group that combines our musical creativity with cutting edge AI technology to create songs that are beautiful and exciting, and aim to point the listener back to our Creator.
            </p>
          </div>
          <div>
            <h3 className="gc-about__h3">What inspires us</h3>
            <p>
              We are deeply moved by the Grace of our Lord Jesus, and we want to remind our listeners of His unending love and mercy through our music. We love to write, and to share our stories, and we hope that we can inspire our listeners to the awe and wonder of creation, and of the One who made it all.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
