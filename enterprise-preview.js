const listElement = document.getElementById("announcement-list");
const searchElement = document.getElementById("company-search");
const countElement = document.getElementById("result-count");
const emptyElement = document.getElementById("empty-state");

function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function searchableText(item) {
    return [
        item.company,
        item.action,
        item.announcementDate,
        item.actionDate,
        item.updatedAt,
        item.affectedMaterial?.name,
        item.affectedMaterial?.batch,
        ...item.products.flatMap(product => [
            product.name,
            product.purchasePeriod,
            product.batchOrExpiry
        ])
    ].filter(Boolean).join(" ").toLocaleLowerCase("zh-TW");
}

function sourceLinks(item) {
    return item.sources.map(source => `
        <a href="${escapeHtml(source.url)}" target="_blank" rel="noopener noreferrer">
            ${escapeHtml(source.label)} ↗
        </a>
    `).join("");
}

function productRows(item) {
    return item.products.map(product => {
        const details = [
            product.purchasePeriod ? `購買期間：${product.purchasePeriod}` : "",
            product.batchOrExpiry ? `批號／效期：${product.batchOrExpiry}` : ""
        ].filter(Boolean).join("　");

        return `
            <div class="product-item">
                <strong>${escapeHtml(product.name)}</strong>
                <span>${escapeHtml(details)}</span>
            </div>
        `;
    }).join("");
}

function render(query = "") {
    const terms = query.trim().toLocaleLowerCase("zh-TW").split(/\s+/).filter(Boolean);
    const results = enterpriseAnnouncementDraft.readyForPreview.filter(item => {
        const text = searchableText(item);
        return terms.every(term => text.includes(term));
    });

    listElement.innerHTML = results.map(item => `
        <article class="announcement-card">
            <div class="card-main">
                <div class="company-meta">
                    <span class="verified-label">A 級證據・官方來源</span>
                    <h3>${escapeHtml(item.company)}</h3>
                    <p class="meta-row">公告日期：${escapeHtml(item.announcementDate)}</p>
                    ${item.actionDate ? `<p class="meta-row">處置日期：${escapeHtml(item.actionDate)}</p>` : ""}
                    ${item.updatedAt ? `<p class="meta-row">更新日期：${escapeHtml(item.updatedAt)}</p>` : ""}
                    <p class="action-text">${escapeHtml(item.action)}</p>
                </div>
                <div>
                    <div class="product-head">
                        <strong>確認產品與批號／效期</strong>
                        <span class="product-count">${item.products.length} 項</span>
                    </div>
                    <div class="product-list">${productRows(item)}</div>
                </div>
            </div>
            <div class="card-footer">
                <span>${escapeHtml(item.evidenceNote)}</span>
                <div class="source-links">${sourceLinks(item)}</div>
            </div>
        </article>
    `).join("");

    countElement.textContent = `顯示 ${results.length}／${enterpriseAnnouncementDraft.readyForPreview.length} 家`;
    emptyElement.hidden = results.length !== 0;
}

searchElement.addEventListener("input", event => render(event.target.value));
document.getElementById("ready-count").textContent = enterpriseAnnouncementDraft.readyForPreview.length;
render();
