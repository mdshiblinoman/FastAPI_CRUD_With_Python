const API_URL = '/users';

// DOM Elements
const userForm = document.getElementById('user-form');
const formTitle = document.getElementById('form-title');
const userIdInput = document.getElementById('user-id');
const nameInput = document.getElementById('name');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const submitBtn = document.getElementById('submit-btn');
const btnText = document.getElementById('btn-text');
const cancelBtn = document.getElementById('cancel-btn');
const refreshBtn = document.getElementById('refresh-btn');
const usersTable = document.getElementById('users-table');
const usersTbody = document.getElementById('users-tbody');
const loading = document.getElementById('loading');
const emptyState = document.getElementById('empty-state');
const toast = document.getElementById('toast');

// State
let isEditMode = false;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    fetchUsers();
});

// Event Listeners
userForm.addEventListener('submit', handleSubmit);
cancelBtn.addEventListener('click', resetForm);
refreshBtn.addEventListener('click', fetchUsers);

// Fetch all users
async function fetchUsers() {
    showLoading(true);
    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error('Failed to fetch users');
        const users = await response.json();
        renderUsers(users);
    } catch (error) {
        showToast('Failed to load users', 'error');
        console.error(error);
    } finally {
        showLoading(false);
    }
}

// Render users table
function renderUsers(users) {
    if (users.length === 0) {
        usersTable.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }

    emptyState.style.display = 'none';
    usersTable.style.display = 'table';

    usersTbody.innerHTML = users.map(user => `
        <tr>
            <td>${user.id}</td>
            <td>${escapeHtml(user.name)}</td>
            <td>${escapeHtml(user.email)}</td>
            <td class="actions">
                <button class="btn btn-edit" onclick="editUser(${user.id}, '${escapeHtml(user.name)}', '${escapeHtml(user.email)}')">
                    ✏️ Edit
                </button>
                <button class="btn btn-delete" onclick="deleteUser(${user.id})">
                    🗑️ Delete
                </button>
            </td>
        </tr>
    `).join('');
}

// Handle form submit (create or update)
async function handleSubmit(e) {
    e.preventDefault();

    const userData = {
        name: nameInput.value.trim(),
        email: emailInput.value.trim(),
        password: passwordInput.value
    };

    try {
        let response;
        if (isEditMode) {
            const userId = userIdInput.value;
            response = await fetch(`${API_URL}/${userId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userData)
            });
            if (!response.ok) throw new Error('Failed to update user');
            showToast('User updated successfully!', 'success');
        } else {
            response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userData)
            });
            if (!response.ok) throw new Error('Failed to create user');
            showToast('User created successfully!', 'success');
        }

        resetForm();
        fetchUsers();
    } catch (error) {
        showToast(error.message, 'error');
        console.error(error);
    }
}

// Edit user - populate form
function editUser(id, name, email) {
    isEditMode = true;
    userIdInput.value = id;
    nameInput.value = name;
    emailInput.value = email;
    passwordInput.value = '';
    passwordInput.placeholder = 'Enter new password';

    formTitle.textContent = 'Edit User';
    btnText.textContent = 'Update User';
    cancelBtn.style.display = 'inline-block';

    // Scroll to form
    document.querySelector('.form-card').scrollIntoView({ behavior: 'smooth' });
}

// Delete user
async function deleteUser(id) {
    if (!confirm('Are you sure you want to delete this user?')) return;

    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error('Failed to delete user');
        showToast('User deleted successfully!', 'success');
        fetchUsers();
    } catch (error) {
        showToast(error.message, 'error');
        console.error(error);
    }
}

// Reset form to add mode
function resetForm() {
    isEditMode = false;
    userForm.reset();
    userIdInput.value = '';
    passwordInput.placeholder = 'Enter password';
    formTitle.textContent = 'Add New User';
    btnText.textContent = 'Add User';
    cancelBtn.style.display = 'none';
}

// Show/hide loading state
function showLoading(show) {
    loading.style.display = show ? 'block' : 'none';
    if (show) {
        usersTable.style.display = 'none';
        emptyState.style.display = 'none';
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    toast.textContent = message;
    toast.className = `toast ${type} show`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
