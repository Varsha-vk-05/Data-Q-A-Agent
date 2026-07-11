import { describe, it, expect } from 'vitest';
import { computeAnswers } from './computeQA';

describe('computeAnswers', () => {
  it('returns an empty array if no data is provided', () => {
    expect(computeAnswers([])).toEqual([]);
    expect(computeAnswers(null)).toEqual([]);
  });

  it('correctly computes answers for a sample dataset', () => {
    const mockData = [
      { Date: '2023-01-01', Region: 'North', Product_Category: 'Electronics', Sales_Revenue: '1000', Units_Sold: '10', Profit: '200' },
      { Date: '2023-01-15', Region: 'South', Product_Category: 'Furniture', Sales_Revenue: '500', Units_Sold: '5', Profit: '100' },
      { Date: '2024-02-10', Region: 'North', Product_Category: 'Electronics', Sales_Revenue: '2000', Units_Sold: '20', Profit: '400' },
    ];

    const answers = computeAnswers(mockData);

    // Should return an array of questions
    expect(answers.length).toBeGreaterThan(0);

    // Q1: Total Revenue
    expect(answers[0].q).toBe('What is the total sales revenue across all regions?');
    expect(answers[0].a).toBe('Total sales revenue is $3,500'); // 1000 + 500 + 2000

    // Q2: Highest profit region
    expect(answers[1].q).toBe('Which region had the highest total profit?');
    expect(answers[1].a).toContain('North'); // 600 vs 100
  });
});
