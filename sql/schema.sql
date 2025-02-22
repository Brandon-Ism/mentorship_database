-- Drop database if it exists to start fresh
DROP DATABASE IF EXISTS mentorship_db;
CREATE DATABASE mentorship_db;
USE mentorship_db;

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    academic_position ENUM('Undergraduate', 'Graduate Student', 'Postdoc', 'Faculty', 'Industry', 'Other') NOT NULL,
    institution VARCHAR(255),
    department VARCHAR(255),
    bio TEXT,
    interested_in SET('Collaboration', 'Providing Mentorship', 'Receiving Mentorship', 'N/A') NOT NULL
);

-- Research Interests Table (Predefined + User-Added)
CREATE TABLE research_interests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

-- Users can have up to 5 research interests (Many-to-Many)
CREATE TABLE user_research_interests (
    user_id INT,
    interest_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (interest_id) REFERENCES research_interests(id) ON DELETE CASCADE
);

-- External Links Table (Up to 5 links per user)
CREATE TABLE user_links (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    link VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Prepopulate Research Interests
INSERT INTO research_interests (name) VALUES
('Algorithm design and analysis'),
('Computational complexity theory'),
('Approximation algorithms'),
('Supervised learning'),
('Unsupervised learning'),
('Reinforcement learning'),
('Natural language processing (NLP)'),
('Databases'),
('Anomaly detection'),
('Computer vision'),
('Explainable AI'),
('User interface design'),
('Usability studies'),
('Augmented and virtual reality'),
('Machine learning'),
('Data mining'),
('Deep learning'),
('Predictive analytics'),
('Data visualization'),
('Public-key cryptography'),
('Blockchain technology'),
('Cybersecurity'),
('Software development life cycle'),
('Agile methodologies'),
('Software testing and verification'),
('Cloud computing'),
('Distributed algorithms'),
('Parallel computing'),
('Internet of Things (IoT)'),
('Network protocols'),
('Data centers'),
('Operating systems'),
('Formal languages and automata'),
('Computability theory'),
('Autonomous robots'),
('Robotic perception and motion planning'),
('Pure Mathematics'),
('Number theory'),
('Algebra'),
('Topology'),
('Geometry'),
('Mathematical logic'),
('Applied Mathematics'),
('Differential equations'),
('Numerical analysis'),
('Mathematical modeling'),
('Optimization'),
('Bayesian inference'),
('Stochastic processes'),
('Hypothesis testing'),
('Time series analysis'),
('Quantum mechanics'),
('General relativity'),
('Nonlinear dynamics and chaos theory'),
('Graph theory'),
('Combinatorial optimization'),
('Financial modeling'),
('Risk management'),
('Stochastic calculus'),
('High-performance computing'),
('Scientific computing'),
('Inferential statistics'),
('Multivariate regression'),
('Cluster analysis'),
('ARIMA models'),
('Predictive modeling'),
('Markov Chain Monte Carlo (MCMC)'),
('Bayesian networks'),
('Random sampling methods'),
('Monte Carlo simulations'),
('Bootstrapping'),
('Statistical modeling'),
('Quantum field theory'),
('String theory'),
('Black holes and singularities'),
('Dark matter and dark energy'),
('Condensed matter physics'),
('Superconductivity'),
('Photonic and magnetic materials'),
('Molecular biophysics'),
('Protein folding'),
('Biomechanics'),
('Fusion research'),
('Fluid dynamics'),
('Field theory'),
('Quantum computing');
