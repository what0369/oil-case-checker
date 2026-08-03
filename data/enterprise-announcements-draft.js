// Draft only. Do not load this file from index.html until the owner approves publication.
// Inclusion rule: a corporate website/social post must confirm the action, and an official
// corporate or government source must identify the affected product and batch/effective date.
const enterpriseAnnouncementDraft = {
  reviewedAt: "2026-08-03",
  publicationStatus: "draft",
  inclusionRule: "企業官網或官方社群確認處置，並由企業或政府官方資料補齊產品及批號／效期",
  readyForPreview: [
    {
      company: "鼎泰豐",
      announcementDate: "2026-07-06",
      action: "主動通知通路下架回收；未出貨商品全數封存；受理退費至2026-08-07",
      evidenceLevel: "A",
      evidenceNote: "企業官網同頁列出產品與有效日期",
      products: [
        { name: "鮮肉／菜肉大包禮盒", batchOrExpiry: "2026.07.25、2026.08.01" },
        { name: "菜肉蒸餃／香菇素餃禮盒", batchOrExpiry: "2026.07.07、2026.07.14" },
        { name: "紅燒牛肉麵禮盒", batchOrExpiry: "2027.04.04、2027.04.18、2027.04.25、2027.05.16" },
        { name: "蝦肉／鮮肉紅油抄手禮盒", batchOrExpiry: "2026.08.26" },
        { name: "菜肉紅油抄手禮盒", batchOrExpiry: "2026.09.03、2026.09.10" },
        { name: "極品豬腳禮盒", batchOrExpiry: "2027.05.17" },
        { name: "香菇素包禮盒", batchOrExpiry: "2026.08.08、2026.08.15" }
      ],
      sources: [
        {
          type: "corporate",
          label: "鼎泰豐聲明公告",
          url: "https://www.dintaifung.com.tw/news_show.php?id=351"
        }
      ]
    },
    {
      company: "路易莎咖啡",
      announcementDate: "2026-07-08",
      actionDate: "2026-07-06",
      action: "全面自主回收、下架、封存，由總公司統一銷毀",
      evidenceLevel: "A",
      evidenceNote: "企業官網確認處置；食藥署官方清單補齊產品與有效日期",
      affectedMaterial: {
        name: "益康大豆沙拉油 18L",
        batch: "20270410000407",
        expiry: "2027.04.10"
      },
      products: [
        { name: "芝麻蜂蜜小蛋糕", batchOrExpiry: "2026.07.06、07.07、07.08、07.11、07.12、07.13、07.14、07.15、07.19、07.21" },
        { name: "焙茶柚香小蛋糕", batchOrExpiry: "2026.07.06、07.07、07.08、07.11、07.12、07.13、07.15、07.18、07.19、07.20" },
        { name: "泰奶波士頓小蛋糕", batchOrExpiry: "2026.07.06、07.07、07.08、07.12、07.14、07.15、07.19、07.21" },
        { name: "抹茶草莓小蛋糕", batchOrExpiry: "2026.07.06、07.07、07.08、07.11、07.12、07.13、07.14、07.15、07.18、07.19、07.21" },
        { name: "焙茶瑪德蓮", batchOrExpiry: "2026.07.06、07.07、07.11、07.13、07.14、07.19" },
        { name: "咖啡小蛋糕", batchOrExpiry: "2026.07.06、07.07、07.08、07.12、07.13、07.14、07.15、07.18、07.19、07.20、07.21" },
        { name: "香草水蜜桃小蛋糕", batchOrExpiry: "2026.07.06、07.07、07.08、07.11、07.12、07.13、07.14、07.15、07.19、07.20、07.21" },
        { name: "檸檬小蛋糕", batchOrExpiry: "2026.07.06、07.08、07.13、07.15、07.18、07.20" },
        { name: "波隆那肉醬", batchOrExpiry: "2026.07.16、08.01、08.04、08.08、08.17、08.31、09.06、09.15、09.24" },
        { name: "印度咖哩醬", batchOrExpiry: "2026.07.27、08.05、08.12、08.15、09.06、09.21" }
      ],
      sources: [
        {
          type: "corporate",
          label: "路易莎集團聲明書",
          url: "https://www.louisacoffee.co/newsDetail/456"
        },
        {
          type: "government",
          label: "食藥署中聯油脂案強制下架／下游產品資料",
          url: "https://www.fda.gov.tw/TC/site13712.aspx"
        }
      ]
    },
    {
      company: "全家便利商店",
      announcementDate: "2026-07-13",
      updatedAt: "2026-07-14",
      action: "依疑慮商品批號辦理退款，受理至2026-09-13",
      evidenceLevel: "A",
      evidenceNote: "企業官網列出商品、購買期間及效期批號",
      products: [
        { name: "黃金魚堡", purchasePeriod: "2026.04.20–05.02", batchOrExpiry: "2026.04.20–05.02" },
        { name: "魔王愛吃辣雞堡", purchasePeriod: "2026.04.20–05.02", batchOrExpiry: "2026.04.20–05.02" },
        { name: "粗飽系雞排炒飯", purchasePeriod: "2026.04.20–05.02", batchOrExpiry: "2026.04.20–05.02" },
        { name: "鐵板滑蛋炸豬排丼", purchasePeriod: "2026.04.20–05.02", batchOrExpiry: "2026.04.20–05.02" },
        { name: "美式雞腿堡", purchasePeriod: "2026.04.20–05.02", batchOrExpiry: "2026.04.20–05.02" },
        { name: "Fami煮煮（主管機關公告品項）", purchasePeriod: "2026.04.20–05.02", batchOrExpiry: "2026.04.20–05.02" },
        { name: "桂冠沙拉", purchasePeriod: "2026.04.09–07.05", batchOrExpiry: "2026.07.08–07.15" },
        { name: "黑胡椒蒜味雞柳條", purchasePeriod: "2026.03.28–04.30", batchOrExpiry: "2026.04.27–04.30" },
        { name: "義式經典嫩雞胸", purchasePeriod: "2026.05.07–06.12", batchOrExpiry: "2026.06.06–06.08、06.10–06.12" }
      ],
      sources: [
        {
          type: "corporate",
          label: "全家便利商店油品事件公告",
          url: "https://www.family.com.tw/ESG/NewsShow?NSNO=202607130000179"
        }
      ]
    }
  ]
};
