const enterpriseList = document.getElementById("enterprise-announcement-list");
const enterpriseSearch = document.getElementById("enterprise-company-search");
const enterpriseCount = document.getElementById("enterprise-result-count");
const enterpriseEmpty = document.getElementById("enterprise-empty-state");

function enterpriseEscape(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function enterpriseSearchText(item) {
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

function enterpriseProductHtml(item) {
    return item.products.map(product => {
        const detail = [
            product.purchasePeriod ? `購買期間：${product.purchasePeriod}` : "",
            product.batchOrExpiry ? `批號／效期：${product.batchOrExpiry}` : ""
        ].filter(Boolean).join("　");
        return `
            <div class="enterprise-product">
                <strong>${enterpriseEscape(product.name)}</strong>
                <span>${enterpriseEscape(detail)}</span>
            </div>
        `;
    }).join("");
}

function enterpriseSourcesHtml(item) {
    return item.sources.map(source => `
        <a href="${enterpriseEscape(source.url)}" target="_blank" rel="noopener noreferrer">
            ${enterpriseEscape(source.label)} ↗
        </a>
    `).join("");
}

function enterpriseAnnouncementCardHtml(item) {
    return `
        <article class="enterprise-card">
            <div class="enterprise-card-main">
                <div class="enterprise-company">
                    <span>A 級證據・企業自主公告</span>
                    <h3>${enterpriseEscape(item.company)}</h3>
                    <p>公告日期：${enterpriseEscape(item.announcementDate)}</p>
                    ${item.actionDate ? `<p>處置日期：${enterpriseEscape(item.actionDate)}</p>` : ""}
                    ${item.updatedAt ? `<p>更新日期：${enterpriseEscape(item.updatedAt)}</p>` : ""}
                    <p class="enterprise-action">${enterpriseEscape(item.action)}</p>
                </div>
                <div>
                    <div class="enterprise-product-head">
                        <strong>確認產品與批號／效期</strong>
                        <span>${item.products.length} 項</span>
                    </div>
                    <div class="enterprise-products">${enterpriseProductHtml(item)}</div>
                </div>
            </div>
            <div class="enterprise-card-footer">
                <span>${enterpriseEscape(item.evidenceNote)}</span>
                <div>${enterpriseSourcesHtml(item)}</div>
            </div>
        </article>
    `;
}

function findEnterpriseAnnouncementMatches(query = "") {
    const terms = query.trim().toLocaleLowerCase("zh-TW").split(/\s+/).filter(Boolean);
    if (terms.length === 0) return [];
    return enterpriseAnnouncementDraft.readyForPreview.filter(item => {
        const text = enterpriseSearchText(item);
        return terms.every(term => text.includes(term));
    });
}

function renderUnifiedEnterpriseResults(results) {
    const section = document.getElementById("unified-enterprise-section");
    const list = document.getElementById("unified-enterprise-results");
    const count = document.getElementById("unified-enterprise-result-count");
    if (!section || !list || !count) return;

    section.classList.toggle("hidden", results.length === 0);
    count.textContent = results.length;
    list.innerHTML = results.map(enterpriseAnnouncementCardHtml).join("");
}

function renderEnterpriseAnnouncements(query = "") {
    const terms = query.trim().toLocaleLowerCase("zh-TW").split(/\s+/).filter(Boolean);
    const results = terms.length === 0
        ? enterpriseAnnouncementDraft.readyForPreview
        : findEnterpriseAnnouncementMatches(query);

    enterpriseList.innerHTML = results.map(enterpriseAnnouncementCardHtml).join("");

    enterpriseCount.textContent = `顯示 ${results.length}／${enterpriseAnnouncementDraft.readyForPreview.length} 家`;
    enterpriseEmpty.hidden = results.length !== 0;
}

enterpriseSearch.addEventListener("input", event => renderEnterpriseAnnouncements(event.target.value));
document.getElementById("enterprise-ready-count").textContent = enterpriseAnnouncementDraft.readyForPreview.length;
renderEnterpriseAnnouncements();
