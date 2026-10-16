import { useParams, Link } from 'react-router-dom';
import './Blog.css';

const BlogPost = () => {
  const { id } = useParams();
  const posts = [
    {
      id: 1,
      title: 'Our Journey with AI Music',
      date: 'October 8, 2025',
      image: 'images/album-covers/your-majesty.jpg?v=3',
      excerpt: 'Discover how Gracechase blends AI creativity with human emotion to create unique music experiences.',
      content: 'Full content for the first post goes here. This is where the detailed article would be displayed. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    },
    {
      id: 2,
      title: 'Behind the Scenes: Creating "Your Majesty"',
      date: 'October 5, 2025',
      image: 'images/site-banners/YMBG.jpg',
      excerpt: 'A deep dive into the inspiration and production process behind our latest album.',
      content: 'Full content for the second post. More details about the album creation process. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
    }
  ];

  const post = posts.find(p => p.id === parseInt(id));

  if (!post) {
    return <div>Post not found</div>;
  }

  return (
    <div className="blog-page">
      <header className="blog-header">
        <Link to="/blog" className="home-link">← Back to Blog</Link>
        <h1>{post.title}</h1>
        <p>{post.date}</p>
      </header>
      <section className="blog-post-full">
        <img src={post.image} alt={post.title} className="blog-post-image-full" />
        <div className="blog-content">
          <p>{post.content}</p>
        </div>
      </section>
    </div>
  );
};

export default BlogPost;