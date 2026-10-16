import { Link } from 'react-router-dom';
import './Blog.css';

const Blog = () => {
  const posts = [
    {
      id: 1,
      title: 'Our Journey with AI Music',
      date: 'October 8, 2025',
      image: 'images/album-covers/your-majesty.jpg?v=3',
      excerpt: 'Discover how Gracechase blends AI creativity with human emotion to create unique music experiences.',
      content: 'Full content for the first post goes here. This is where the detailed article would be displayed.'
    },
    {
      id: 2,
      title: 'Behind the Scenes: Creating "Your Majesty"',
      date: 'October 5, 2025',
      image: 'images/site-banners/YMBG.jpg',
      excerpt: 'A deep dive into the inspiration and production process behind our latest album.',
      content: 'Full content for the second post. More details about the album creation process.'
    }
  ];

  return (
    <div className="blog-page">
      <header className="blog-header">
        <Link to="/" className="home-link">← Back to Home</Link>
        <h1>Blog</h1>
        <p>Insights, stories, and updates from Gracechase</p>
      </header>
      <section className="blog-posts">
        {posts.map(post => (
          <article key={post.id} className="blog-post">
            <img src={post.image} alt={post.title} className="blog-post-image" />
            <h2><Link to={`/blog/${post.id}`} className="post-link">{post.title}</Link></h2>
            <p className="post-date">{post.date}</p>
            <p className="post-excerpt">{post.excerpt}</p>
            <Link to={`/blog/${post.id}`} className="read-more">Read More</Link>
          </article>
        ))}
      </section>
    </div>
  );
};

export default Blog;