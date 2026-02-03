const USERS_KEY = 'lypa_users';
const DATA_KEY = 'lypa_data';

async function hashPassword(password) {
  const encoder = new TextEncoder();
  const data = encoder.encode(password);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

function getUsers() {
  const raw = localStorage.getItem(USERS_KEY);
  return raw ? JSON.parse(raw) : {};
}

function saveUsers(users) {
  localStorage.setItem(USERS_KEY, JSON.stringify(users));
}

function getData() {
  const raw = localStorage.getItem(DATA_KEY);
  return raw ? JSON.parse(raw) : {};
}

function saveData(data) {
  localStorage.setItem(DATA_KEY, JSON.stringify(data));
}

function validateUsername(username) {
  if (username.length < 3 || username.length > 30) {
    return 'Username must be 3-30 characters.';
  }
  if (!/^[a-zA-Z][a-zA-Z0-9]*$/.test(username)) {
    return 'Username must start with a letter and contain only letters and numbers.';
  }
  return null;
}

function validateEmail(email) {
  if (email.length < 10) {
    return 'Email is too short.';
  }
  const parts = email.split('@');
  if (parts.length !== 2) {
    return 'Invalid email format.';
  }
  if (!parts[1].includes('.')) {
    return 'Invalid email domain.';
  }
  return null;
}

export async function register(email, username, password, confirmPassword) {
  if (password.length < 6) {
    return { success: false, error: 'Password must be at least 6 characters.' };
  }
  if (password !== confirmPassword) {
    return { success: false, error: 'Passwords do not match.' };
  }

  const usernameError = validateUsername(username);
  if (usernameError) {
    return { success: false, error: usernameError };
  }

  const emailError = validateEmail(email);
  if (emailError) {
    return { success: false, error: emailError };
  }

  const users = getUsers();
  const lowerUsername = username.toLowerCase();

  if (users[lowerUsername]) {
    return { success: false, error: 'Username already exists.' };
  }

  const emailExists = Object.values(users).some(u => u.email === email.toLowerCase());
  if (emailExists) {
    return { success: false, error: 'Email already registered.' };
  }

  const hashedPassword = await hashPassword(password);
  users[lowerUsername] = {
    email: email.toLowerCase(),
    password: hashedPassword,
  };
  saveUsers(users);

  return { success: true };
}

export async function login(identifier, password) {
  const users = getUsers();
  const hashedPassword = await hashPassword(password);
  const lowerIdentifier = identifier.toLowerCase();

  // Check by username
  if (users[lowerIdentifier] && users[lowerIdentifier].password === hashedPassword) {
    return { success: true, username: lowerIdentifier };
  }

  // Check by email
  for (const [username, user] of Object.entries(users)) {
    if (user.email === lowerIdentifier && user.password === hashedPassword) {
      return { success: true, username };
    }
  }

  return { success: false, error: 'Invalid username/email or password.' };
}

export function addTestResult(username, wpm, accuracy) {
  const data = getData();
  const key = username.toLowerCase();
  if (!data[key]) {
    data[key] = { wpm: [], accuracy: [] };
  }
  data[key].wpm.push(wpm);
  data[key].accuracy.push(accuracy);
  saveData(data);
}

export function getTestResults(username) {
  const data = getData();
  const key = username.toLowerCase();
  return data[key] || { wpm: [], accuracy: [] };
}
