-- Add comments table
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY,
    post_id INTEGER,
    user_id INTEGER,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Insert sample users if not exists
INSERT OR IGNORE INTO users (id, name, email, created_at) VALUES
    (1, 'John Doe', 'john@example.com', datetime('now', '-60 days')),
    (2, 'Jane Smith', 'jane@example.com', datetime('now', '-45 days')),
    (3, 'Bob Wilson', 'bob@example.com', datetime('now', '-15 days')),
    (4, 'Alice Brown', 'alice@example.com', datetime('now', '-10 days')),
    (5, 'Charlie Davis', 'charlie@example.com', datetime('now', '-5 days'));

-- Insert sample posts
INSERT OR IGNORE INTO posts (id, user_id, title, content, created_at) VALUES
    (1, 1, 'First Post', 'Hello World!', datetime('now', '-40 days')),
    (2, 1, 'Second Post', 'Another post by John', datetime('now', '-35 days')),
    (3, 2, 'Jane''s Post', 'Hello from Jane', datetime('now', '-30 days')),
    (4, 3, 'Bob''s Post', 'New here!', datetime('now', '-12 days')),
    (5, 4, 'Alice''s Post', 'My first post', datetime('now', '-8 days')),
    (6, 3, 'Another from Bob', 'Getting the hang of this', datetime('now', '-5 days'));

-- Insert sample comments
INSERT OR IGNORE INTO comments (post_id, user_id, content, created_at) VALUES
    -- Comments on John's posts
    (1, 2, 'Welcome!', datetime('now', '-39 days')),
    (1, 3, 'Great first post!', datetime('now', '-39 days')),
    (1, 1, 'Thanks everyone!', datetime('now', '-38 days')), -- John commenting on his own post
    (2, 4, 'Nice post!', datetime('now', '-34 days')),
    (2, 1, 'Glad you liked it!', datetime('now', '-34 days')), -- John commenting on his own post
    
    -- Comments on Jane's post
    (3, 1, 'Hi Jane!', datetime('now', '-29 days')),
    (3, 2, 'Thanks John!', datetime('now', '-29 days')), -- Jane commenting on her own post
    (3, 3, 'Great community!', datetime('now', '-28 days')),
    
    -- Comments on Bob's posts
    (4, 4, 'Welcome Bob!', datetime('now', '-11 days')),
    (4, 3, 'Thanks!', datetime('now', '-11 days')), -- Bob commenting on his own post
    (6, 3, 'Getting better!', datetime('now', '-4 days')), -- Bob commenting on his own post
    (6, 5, 'Keep it up!', datetime('now', '-4 days')),
    
    -- Comments on Alice's post
    (5, 3, 'Welcome Alice!', datetime('now', '-7 days')),
    (5, 4, 'Thank you!', datetime('now', '-7 days')), -- Alice commenting on her own post
    (5, 5, 'Great post!', datetime('now', '-6 days')); 