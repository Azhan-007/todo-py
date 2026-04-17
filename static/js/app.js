/* ═══════════════════════════════════════════════════════════════════════
   TO-DO LIST APP — Client-Side JavaScript
   ═══════════════════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

    // ── Search with debounce ──────────────────────────────────────────
    const searchInput = document.getElementById('search-input');
    let searchTimeout;

    if (searchInput) {
        searchInput.addEventListener('input', () => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                const query = searchInput.value.trim();
                if (query.length > 0) {
                    window.location.href = `/search?q=${encodeURIComponent(query)}`;
                } else {
                    window.location.href = '/';
                }
            }, 500);
        });
    }

    // ── Edit Modal Logic ─────────────────────────────────────────────
    const modal = document.getElementById('edit-modal');
    const editForm = document.getElementById('edit-form');

    // Open edit modal
    document.querySelectorAll('.btn-edit').forEach(btn => {
        btn.addEventListener('click', () => {
            const id = btn.dataset.id;
            const title = btn.dataset.title;
            const desc = btn.dataset.desc;
            const priority = btn.dataset.priority;

            editForm.action = `/update/${id}`;
            document.getElementById('edit-title').value = title;
            document.getElementById('edit-desc').value = desc;
            document.getElementById('edit-priority').value = priority;

            modal.classList.add('active');
        });
    });

    // Close modal
    document.getElementById('modal-close')?.addEventListener('click', () => {
        modal.classList.remove('active');
    });

    // Close on overlay click
    modal?.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
        }
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal?.classList.contains('active')) {
            modal.classList.remove('active');
        }
    });

    // ── Delete confirmation ──────────────────────────────────────────
    document.querySelectorAll('.btn-delete-form').forEach(form => {
        form.addEventListener('submit', (e) => {
            const taskTitle = form.dataset.title;
            if (!confirm(`Delete "${taskTitle}"?`)) {
                e.preventDefault();
            }
        });
    });

});
