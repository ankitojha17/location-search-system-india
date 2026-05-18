# 📍 Location Intelligence & Asynchronous Background Processing System

A high-performance, **production-grade**, non-blocking Django-based REST API designed to handle high-traffic location queries. The system intelligently decouples heavy third-party API lookups from the main request-response cycle using an **Asynchronous Task Queue** and an **Always-On Background Worker**. It features an advanced **Two-Tier Caching Mechanism** to optimize data delivery speeds down to sub-milliseconds.

---

## 🚀 Key Features & Advanced Engineering Concepts

* **Non-Blocking REST Architecture:** The main API instantly responds with a `202 PROCESSING` status for new queries, preventing HTTP connection timeouts and freeing up server threads immediately.
* **Persistent Background Worker (Daemon Process):** Implemented via a custom Django management command that continuously polls the database queue (`SearchLog`) with an optimized polling interval to handle long-running tasks asynchronously.
* **Smart Fuzzy Matching & Autocomplete:** Built-in resilience to handle partial or misspelled queries (e.g., searching `"bux"` automatically resolves to `"Buxar"`) by leveraging external search suggestion scoring.
* **Two-Tier Cache-Aside Pattern:** Integrated memory caching layer (`django.core.cache`) with an automatic expiry window (TTL: 1 Hour). This completely circumvents database and third-party API hits for repetitive traffic, serving cached locations instantly.
* **Dynamic Content Parsing & State Detection:** Implements automated parsing over unstructured text descriptions to run algorithmic matches against strict geographic boundaries (Indian States/UTs metadata mapping).

---

## 🛠️ Tech Stack & System Components

* **Core Framework:** Python / Django / Django REST Framework (DRF)
* **Database Management:** PostgreSQL / SQLite (Engineered with unique indexes and `db_index=True` optimization for fast lookup performance)
* **Caching Layer:** High-speed RAM / Memory Caching (Production-ready for Redis or Memcached backends)
* **External Scraper Engine:** Python Wikipedia API Integration (Engineered with Multi-Step Fallback Search Terms)

---

## 🔄 System Architecture & Flow Lifecycle



1. **API Hit:** User calls `/api/location/?query=bux`.
2. **Tier 1 Cache Check:** The application layer checks the memory cache (`loc_bux`). If found, data is returned instantly (**Time Complexity: $O(1)$**).
3. **Tier 2 Database Check:** On a cache miss, it checks the local database using case-insensitive partial indexing. If a record exists, it populates the cache and returns the data.
4. **Async Task Queuing:** If data is completely missing, the system registers a `PENDING` ticket in the `SearchLog` table and immediately returns a `202 Status` message to the user.
5. **Background Process Lifecycle:** The persistent background worker picks up the `PENDING` ticket, negotiates with the Wikipedia API via an iterative search strategy, executes state detection, updates the core tables, warms up the RAM cache, and sets `is_processed=True`.
6. **Subsequent Fetch:** When the user or any other client checks again, the data is served directly from the cache instantly.

---

## 💻 Installation, Dependencies & Environment Setup

### 1. Clone and Navigate to the Repository
```bash
git clone [https://github.com/ankitojha17/location-search-system-india.git](https://github.com/ankitojha17/location-search-system-india.git)
cd location-search-system-india