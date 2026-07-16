/**
 * KALF Blog Engine
 * Updated to fetch from live API
 */

const BASE_URL = "https://kalf-backend.onrender.com/api/V1";
let allPosts = [];
const blogGrid = document.getElementById("blog-grid");
const filterBtns = document.querySelectorAll(".filter-btn");
const searchInput = document.getElementById("blog-search");

// ── Fetch blogs from live API ──────────────────────────────────
async function initBlog() {
  try {
    blogGrid.innerHTML = `
      <div class="col-span-3 flex flex-col items-center justify-center py-20 text-on-surface-variant dark:text-white/40">
        <span class="material-symbols-outlined text-[48px] animate-spin mb-4">progress_activity</span>
        <p class="text-sm">Loading stories...</p>
      </div>
    `;

    const res = await fetch(`${BASE_URL}/admin/all/blogs`);
    const data = await res.json();

    // Only show published blogs (status === true)
    allPosts = (data.result || []).filter((post) => post.status === true);

    renderBlog("All");
    renderFilterButtons();
  } catch (err) {
    console.error("Blog load error:", err);
    blogGrid.innerHTML = `
      <div class="col-span-3 flex flex-col items-center justify-center py-20 text-on-surface-variant dark:text-white/40">
        <span class="material-symbols-outlined text-[48px] mb-4">error</span>
        <p class="text-sm">Failed to load stories. Please try again.</p>
      </div>
    `;
  }
}

// ── Render filter buttons dynamically from categories ──────────
function renderFilterButtons() {
  const filterContainer = document.getElementById("blog-filters");
  if (!filterContainer) return;

  // Get unique categories from posts
  const categories = [
    ...new Set(allPosts.map((p) => p.category?.name).filter(Boolean)),
  ];

  // Reset to just "All Stories" button
  filterContainer.innerHTML = `
    <button data-category="All" class="filter-btn px-5 py-2 rounded-full bg-primary text-white text-sm font-medium transition-all">
      All Stories
    </button>
  `;

  categories.forEach((cat) => {
    filterContainer.innerHTML += `
      <button data-category="${cat}" class="filter-btn px-5 py-2 rounded-full bg-surface-container dark:bg-white/5 text-sm font-medium transition-all">
        ${cat}
      </button>
    `;
  });

  // Re-attach filter listeners
  document.querySelectorAll(".filter-btn").forEach((btn) => {
    btn.addEventListener("click", () => renderBlog(btn.dataset.category));
  });
}

// ── Create blog card ───────────────────────────────────────────
function createBlogCard(post) {
  const categoryName = post.category?.name || "General";
  const image = post.image || "https://placehold.co/600x400";
  const excerpt = post.content
    ? post.content.substring(0, 120) + "..."
    : "Read this story from the KALF foundation.";
  const date = new Date(post.created_at).toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
  const postId = post.id;

  return `
    <div class="bg-surface-container-lowest dark:bg-white/5 rounded-xl border dark:border-white/10 overflow-hidden group flex flex-col hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
      <div class="h-56 w-full overflow-hidden">
        <img 
          class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" 
          src="${image}" 
          alt="${post.title}"
          onerror="this.src='https://placehold.co/600x400'"
        />
      </div>
      <div class="p-8 flex flex-col flex-grow">
        <span class="text-secondary font-bold uppercase tracking-widest mb-3 block text-[10px]">${categoryName}</span>
        <h3 class="text-xl font-serif font-bold mb-3 leading-tight group-hover:text-secondary transition-colors dark:text-white">
          ${post.title}
        </h3>
        <p class="dark:text-outline text-on-surface-variant text-sm mb-6 leading-relaxed line-clamp-3 flex-grow">
          ${excerpt}
        </p>
        <div class="flex items-center justify-between mt-auto">
          <span class="text-xs text-outline dark:text-white/40">${date}</span>
          <a class="text-secondary font-bold text-sm inline-flex items-center gap-2 group/link" href="/blog/${postId}">
            Read More 
            <span class="material-symbols-outlined text-sm group-hover/link:translate-x-1 transition-transform">arrow_forward</span>
          </a>
        </div>
      </div>
    </div>
  `;
}

// ── Render blog grid ───────────────────────────────────────────
function renderBlog(category, query = "") {
  blogGrid.classList.add("opacity-0");

  setTimeout(() => {
    let filtered = [...allPosts];

    if (category !== "All") {
      filtered = filtered.filter((p) => p.category?.name === category);
    }

    if (query) {
      filtered = filtered.filter((p) =>
        p.title.toLowerCase().includes(query.toLowerCase()),
      );
    }

    if (filtered.length === 0) {
      blogGrid.innerHTML = `
        <div class="col-span-3 flex flex-col items-center justify-center py-20 text-on-surface-variant dark:text-white/40">
          <span class="material-symbols-outlined text-[48px] mb-4">search_off</span>
          <p class="text-sm">No stories found.</p>
        </div>
      `;
    } else {
      blogGrid.innerHTML = filtered.map((p) => createBlogCard(p)).join("");
    }

    updateFilterUI(category);
    blogGrid.classList.remove("opacity-0");
  }, 300);
}

// ── Update filter button UI ────────────────────────────────────
function updateFilterUI(activeCat) {
  document.querySelectorAll(".filter-btn").forEach((btn) => {
    const isActive = btn.dataset.category === activeCat;
    if (isActive) {
      btn.classList.add("bg-primary", "dark:bg-secondary", "text-white");
      btn.classList.remove(
        "bg-surface-container",
        "dark:bg-white/5",
        "text-outline",
      );
    } else {
      btn.classList.remove("bg-primary", "dark:bg-secondary", "text-white");
      btn.classList.add(
        "bg-surface-container",
        "dark:bg-white/5",
        "text-outline",
      );
    }
  });
}

// ── Search listener ────────────────────────────────────────────
searchInput?.addEventListener("input", (e) => {
  const activeBtn = document.querySelector(".filter-btn.bg-primary");
  const activeCat = activeBtn ? activeBtn.dataset.category : "All";
  renderBlog(activeCat, e.target.value);
});

// ── Init ───────────────────────────────────────────────────────
initBlog();
