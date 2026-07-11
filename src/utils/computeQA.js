// Computes answers based on the parsed CSV data array and generates 50+ questions

export function computeAnswers(data) {
  if (!data || data.length === 0) return [];

  // Helper to group by and sum
  const sumBy = (key, valueKey) => {
    return data.reduce((acc, row) => {
      const k = row[key];
      const v = parseFloat(row[valueKey]) || 0;
      if (!acc[k]) acc[k] = 0;
      acc[k] += v;
      return acc;
    }, {});
  };

  // Helper to generate ascii table
  const makeTable = (rows, cols) => {
    if (!rows || rows.length === 0) return "No data";
    const widths = cols.map(c => Math.max(c.length, ...rows.map(r => String(r[c] || "").length)));
    const header = cols.map((c, i) => c.padEnd(widths[i])).join(" | ");
    const divider = widths.map(w => "-".repeat(w)).join("-|-");
    const body = rows.map(r => cols.map((c, i) => String(r[c] || "").padEnd(widths[i])).join(" | ")).join("\n");
    return `${header}\n${divider}\n${body}`;
  };

  const questions = [];

  // 1. Total Revenue
  const totalRevenue = data.reduce((sum, row) => sum + (parseFloat(row.Sales_Revenue) || 0), 0);
  questions.push({
    q: "What is the total sales revenue across all regions?",
    a: `Total sales revenue is $${totalRevenue.toLocaleString()}`,
    table: makeTable(data.map(r => ({...r, Sales_Revenue: `$${r.Sales_Revenue}`})), ['Date', 'Region', 'Product_Category', 'Sales_Revenue'])
  });

  // 2. Highest Profit Region
  const profitByRegion = sumBy('Region', 'Profit');
  const sortedRegions = Object.entries(profitByRegion).sort((a, b) => b[1] - a[1]);
  questions.push({
    q: "Which region had the highest total profit?",
    a: `The ${sortedRegions[0][0]} region had the highest total profit at $${sortedRegions[0][1].toLocaleString()}`,
    table: `Region   | Profit\n------------------\n` + sortedRegions.map(([r, p]) => `${r.padEnd(8)} | $${p}`).join('\n')
  });

  // 3. Top selling product categories
  const unitsByCategory = sumBy('Product_Category', 'Units_Sold');
  const sortedCategories = Object.entries(unitsByCategory).sort((a, b) => b[1] - a[1]);
  questions.push({
    q: "What are the top selling product categories by units sold?",
    a: ``,
    table: `Category     | Units Sold\n-------------------------\n` + sortedCategories.map(([c, u]) => `${c.padEnd(12)} | ${u}`).join('\n')
  });

  // Unique lists for dynamic generation
  const regions = [...new Set(data.map(r => r.Region))];
  const categories = [...new Set(data.map(r => r.Product_Category))];
  const dates = [...new Set(data.map(r => r.Date))].sort();
  const months = [...new Set(data.map(r => r.Date.substring(0, 7)))].sort();

  // Strategy A: Total Sales Revenue per Region (4 questions)
  regions.forEach(region => {
    const rData = data.filter(r => r.Region === region);
    const rSales = rData.reduce((sum, row) => sum + parseFloat(row.Sales_Revenue), 0);
    questions.push({
      q: `What is the total sales revenue for the ${region} region?`,
      a: `The total sales revenue for the ${region} region is $${rSales.toLocaleString()}.`,
      table: makeTable(rData, ['Date', 'Product_Category', 'Sales_Revenue'])
    });
  });

  // Strategy B: Total Units Sold per Category (3 questions)
  categories.forEach(category => {
    const cData = data.filter(r => r.Product_Category === category);
    const cUnits = cData.reduce((sum, row) => sum + parseFloat(row.Units_Sold), 0);
    questions.push({
      q: `How many units of ${category} were sold in total?`,
      a: `A total of ${cUnits.toLocaleString()} units of ${category} were sold.`,
      table: makeTable(cData, ['Date', 'Region', 'Units_Sold'])
    });
  });

  // Strategy C: Cross Section - Units Sold for Category in Region (12 questions)
  regions.forEach(region => {
    categories.forEach(category => {
      const crossData = data.filter(r => r.Region === region && r.Product_Category === category);
      const crossUnits = crossData.reduce((sum, row) => sum + parseFloat(row.Units_Sold), 0);
      questions.push({
        q: `How many units of ${category} were sold in the ${region} region?`,
        a: `${crossUnits} units of ${category} were sold in the ${region} region.`,
        table: makeTable(crossData, ['Date', 'Units_Sold', 'Sales_Revenue', 'Profit'])
      });
    });
  });

  // Strategy D: Cross Section - Profit for Category in Region (12 questions)
  regions.forEach(region => {
    categories.forEach(category => {
      const crossData = data.filter(r => r.Region === region && r.Product_Category === category);
      const crossProfit = crossData.reduce((sum, row) => sum + parseFloat(row.Profit), 0);
      questions.push({
        q: `What was the total profit for ${category} in the ${region} region?`,
        a: `The total profit for ${category} in the ${region} region was $${crossProfit.toLocaleString()}.`,
        table: makeTable(crossData, ['Date', 'Sales_Revenue', 'Profit'])
      });
    });
  });

  // Strategy E: Profit Margin for each category (3 questions)
  categories.forEach(category => {
    const cData = data.filter(r => r.Product_Category === category);
    const cProfit = cData.reduce((sum, row) => sum + parseFloat(row.Profit), 0);
    const cSales = cData.reduce((sum, row) => sum + parseFloat(row.Sales_Revenue), 0);
    const margin = cSales > 0 ? ((cProfit / cSales) * 100).toFixed(2) : 0;
    questions.push({
      q: `What is the average profit margin for ${category}?`,
      a: `The average profit margin for ${category} is ${margin}%.`,
      table: makeTable(cData, ['Date', 'Region', 'Sales_Revenue', 'Profit'])
    });
  });

  // Strategy F: Monthly Sales Total (15 questions if 15 months)
  months.forEach(month => {
    const mData = data.filter(r => r.Date.startsWith(month));
    const mSales = mData.reduce((sum, row) => sum + parseFloat(row.Sales_Revenue), 0);
    questions.push({
      q: `What was the total sales revenue in ${month}?`,
      a: `The total sales revenue in ${month} was $${mSales.toLocaleString()}.`,
      table: makeTable(mData, ['Date', 'Region', 'Product_Category', 'Sales_Revenue'])
    });
  });

  // Strategy G: Average Sale value per region (4 questions)
  regions.forEach(region => {
    const rData = data.filter(r => r.Region === region);
    const rSales = rData.reduce((sum, row) => sum + parseFloat(row.Sales_Revenue), 0);
    const avg = rData.length > 0 ? (rSales / rData.length).toFixed(2) : 0;
    questions.push({
      q: `What is the average transaction value in the ${region} region?`,
      a: `The average transaction value in the ${region} region is $${avg}.`,
      table: makeTable(rData, ['Date', 'Product_Category', 'Sales_Revenue'])
    });
  });

  // Strategy H: Find highest single transaction profit
  let maxProfit = -1;
  let maxRow = null;
  data.forEach(r => {
    const p = parseFloat(r.Profit);
    if (p > maxProfit) {
      maxProfit = p;
      maxRow = r;
    }
  });
  if (maxRow) {
    questions.push({
      q: "Which single transaction had the highest profit?",
      a: `The highest single profit was $${maxProfit.toLocaleString()}, occurring on ${maxRow.Date} in the ${maxRow.Region} region for ${maxRow.Product_Category}.`,
      table: makeTable([maxRow], ['Date', 'Region', 'Product_Category', 'Sales_Revenue', 'Profit'])
    });
  }

  // Strategy I: Find highest single transaction revenue
  let maxRev = -1;
  let maxRevRow = null;
  data.forEach(r => {
    const rev = parseFloat(r.Sales_Revenue);
    if (rev > maxRev) {
      maxRev = rev;
      maxRevRow = r;
    }
  });
  if (maxRevRow) {
    questions.push({
      q: "Which single transaction had the highest sales revenue?",
      a: `The highest single sales revenue was $${maxRev.toLocaleString()}, occurring on ${maxRevRow.Date} in the ${maxRevRow.Region} region for ${maxRevRow.Product_Category}.`,
      table: makeTable([maxRevRow], ['Date', 'Region', 'Product_Category', 'Sales_Revenue', 'Profit'])
    });
  }

  return questions;
}
