// 食藥署 115 年 7 月 21 日重新上架評估結果。
// 7 批不得上架名單另以 115 年 7 月 23 日公布的泰山、福懋、福壽清單交叉核對。
const batchStatusDatabase = [
    { batch: "315-1150404", status: "blocked", label: "不得上架／啟動銷毀" },
    { batch: "318-1150406", status: "blocked", label: "不得上架／啟動銷毀" },
    { batch: "313-1150408", status: "blocked", label: "不得上架／啟動銷毀" },
    { batch: "314-1150410", status: "blocked", label: "不得上架／啟動銷毀" },
    { batch: "315-1150413", status: "blocked", label: "不得上架／啟動銷毀" },
    { batch: "315-1150510", status: "blocked", label: "不得上架／啟動銷毀" },
    { batch: "313-1150512", status: "blocked", label: "不得上架／啟動銷毀" },

    { batch: "314-1150401", status: "relisted", label: "符合規定／可重新上架" },
    { batch: "318-1150415", status: "relisted", label: "符合規定／可重新上架" },
    { batch: "313-1150420", status: "relisted", label: "符合規定／可重新上架" },
    { batch: "314-1150425", status: "relisted", label: "符合規定／可重新上架" },
    { batch: "315-1150428", status: "relisted", label: "符合規定／可重新上架" },
    { batch: "316-1150504", status: "relisted", label: "符合規定／可重新上架" },
    { batch: "314-1150507", status: "relisted", label: "符合規定／可重新上架" },
    { batch: "316-1150515", status: "relisted", label: "符合規定／可重新上架" },
    { batch: "318-1150517", status: "relisted", label: "符合規定／可重新上架" },
    { batch: "314-1150518", status: "relisted", label: "符合規定／可重新上架" },
    { batch: "315-1150521", status: "relisted", label: "符合規定／可重新上架" },
    { batch: "319-1150522", status: "relisted", label: "符合規定／可重新上架" },
    { batch: "318-1150524", status: "relisted", label: "符合規定／可重新上架" },
    { batch: "314-1150608", status: "relisted", label: "符合規定／可重新上架" },
    { batch: "316-1150609", status: "relisted", label: "符合規定／可重新上架" },
    { batch: "319-1150609", status: "relisted", label: "符合規定／可重新上架" },
    { batch: "315-1150614", status: "relisted", label: "符合規定／可重新上架" },
    { batch: "314-1150617", status: "relisted", label: "符合規定／可重新上架" },
    { batch: "316-1150623", status: "relisted", label: "符合規定／可重新上架" },

    { batch: "315-1150626", status: "held", label: "檢驗合格／未出貨留置管制" },
    { batch: "313-1150628", status: "held", label: "檢驗合格／未出貨留置管制" },
    { batch: "318-1150630", status: "held", label: "檢驗合格／未出貨留置管制" },

    { batch: "319-1150613", status: "no-specimen", label: "外銷無檢體／不得恢復上架" }
];

const officialListSnapshot = {
    forcedOperatorsUpdatedAt: "2026/07/22 13:34",
    forcedOperatorRows: 5139,
    forcedOperatorPages: 257,
    relistedProductsUpdatedAt: "2026/07/24 08:19",
    relistedProductRows: 501
};
