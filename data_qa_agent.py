import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
import re

class DataQAAgent:
    def __init__(self, csv_path: str):
        """Initialize the agent with a CSV file."""
        self.df = pd.read_csv(csv_path)
        self.computation_log = []
        
    def get_data_info(self) -> Dict[str, Any]:
        """Get basic information about the dataset."""
        return {
            'shape': self.df.shape,
            'columns': list(self.df.columns),
            'dtypes': self.df.dtypes.to_dict(),
            'sample': self.df.head().to_dict()
        }
    
    def log_computation(self, question: str, computation: str, result: Any):
        """Log how a computation was performed."""
        self.computation_log.append({
            'question': question,
            'computation': computation,
            'result': result
        })
    
    def answer_question(self, question: str) -> Dict[str, Any]:
        """
        Answer a natural language question about the data.
        Returns answer, computation explanation, and supporting data.
        """
        question_lower = question.lower()
        
        # Question patterns and their corresponding computations
        # Check specific patterns first before general ones
        if 'fastest' in question_lower and ('grow' in question_lower or 'grew' in question_lower or 'growth' in question_lower):
            return self._calculate_growth_rate(question)
        elif 'satisfaction' in question_lower:
            return self._analyze_satisfaction(question)
        elif 'profit' in question_lower:
            return self._analyze_profit(question)
        elif 'highest' in question_lower or 'most' in question_lower:
            return self._find_highest(question)
        elif 'lowest' in question_lower or 'least' in question_lower:
            return self._find_lowest(question)
        elif 'average' in question_lower or 'mean' in question_lower:
            return self._calculate_average(question)
        elif 'total' in question_lower or 'sum' in question_lower:
            return self._calculate_total(question)
        elif 'compare' in question_lower or 'difference' in question_lower:
            return self._compare_values(question)
        elif 'best' in question_lower:
            return self._find_best(question)
        elif 'worst' in question_lower:
            return self._find_worst(question)
        else:
            return self._general_query(question)
    
    def _calculate_growth_rate(self, question: str) -> Dict[str, Any]:
        """Calculate growth rates between quarters."""
        try:
            # Extract time period from question
            if 'last quarter' in question.lower():
                # Compare Q3 to Q4 (last quarter growth)
                q3_data = self.df[self.df['Quarter'] == 'Q3 2024']
                q4_data = self.df[self.df['Quarter'] == 'Q4 2024']
                
                q3_revenue = q3_data.groupby('Region')['Revenue'].sum()
                q4_revenue = q4_data.groupby('Region')['Revenue'].sum()
                
                growth_rates = ((q4_revenue - q3_revenue) / q3_revenue * 100).round(2)
                fastest_region = growth_rates.idxmax()
                fastest_rate = growth_rates.max()
                
                computation = f"Calculated Q4 vs Q3 revenue growth by region: ((Q4_Revenue - Q3_Revenue) / Q3_Revenue) * 100"
                self.log_computation(question, computation, fastest_rate)
                
                return {
                    'answer': f"{fastest_region} region grew fastest last quarter with {fastest_rate}% growth",
                    'computation': computation,
                    'supporting_data': {
                        'growth_rates_by_region': growth_rates.to_dict(),
                        'q3_revenue': q3_revenue.to_dict(),
                        'q4_revenue': q4_revenue.to_dict()
                    }
                }
            else:
                # Calculate overall quarterly growth
                quarters = ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024']
                quarterly_revenue = [self.df[self.df['Quarter'] == q]['Revenue'].sum() for q in quarters]
                
                growth_rates = []
                for i in range(1, len(quarters)):
                    growth = ((quarterly_revenue[i] - quarterly_revenue[i-1]) / quarterly_revenue[i-1] * 100)
                    growth_rates.append(growth)
                
                max_growth_idx = np.argmax(growth_rates)
                fastest_quarter = quarters[max_growth_idx + 1]
                fastest_rate = round(growth_rates[max_growth_idx], 2)
                
                computation = f"Calculated sequential quarterly growth: ((Current_Quarter - Previous_Quarter) / Previous_Quarter) * 100"
                self.log_computation(question, computation, fastest_rate)
                
                return {
                    'answer': f"{fastest_quarter} grew fastest with {fastest_rate}% growth",
                    'computation': computation,
                    'supporting_data': {
                        'quarterly_revenue': dict(zip(quarters, quarterly_revenue)),
                        'growth_rates': dict(zip(quarters[1:], growth_rates))
                    }
                }
        except Exception as e:
            return {
                'answer': f"Error calculating growth rate: {str(e)}",
                'computation': f"Error in growth calculation: {str(e)}",
                'supporting_data': {}
            }
    
    def _find_highest(self, question: str) -> Dict[str, Any]:
        """Find the highest value for a metric."""
        if 'revenue' in question.lower():
            if 'region' in question.lower():
                region_revenue = self.df.groupby('Region')['Revenue'].sum()
                highest_region = region_revenue.idxmax()
                highest_value = region_revenue.max()
                
                computation = "Summed Revenue by Region and found maximum"
                self.log_computation(question, computation, highest_value)
                
                return {
                    'answer': f"{highest_region} region has the highest total revenue at ${highest_value:,.0f}",
                    'computation': computation,
                    'supporting_data': {
                        'revenue_by_region': region_revenue.to_dict()
                    }
                }
            elif 'product' in question.lower():
                product_revenue = self.df.groupby('Product')['Revenue'].sum()
                highest_product = product_revenue.idxmax()
                highest_value = product_revenue.max()
                
                computation = "Summed Revenue by Product and found maximum"
                self.log_computation(question, computation, highest_value)
                
                return {
                    'answer': f"{highest_product} has the highest total revenue at ${highest_value:,.0f}",
                    'computation': computation,
                    'supporting_data': {
                        'revenue_by_product': product_revenue.to_dict()
                    }
                }
        
        # Default: find max in entire dataset
        max_row = self.df.loc[self.df['Revenue'].idxmax()]
        computation = "Found row with maximum Revenue value"
        self.log_computation(question, computation, max_row['Revenue'])
        
        return {
            'answer': f"Highest revenue record: {max_row['Region']}, {max_row['Quarter']}, {max_row['Product']} with ${max_row['Revenue']:,.0f}",
            'computation': computation,
            'supporting_data': max_row.to_dict()
        }
    
    def _find_lowest(self, question: str) -> Dict[str, Any]:
        """Find the lowest value for a metric."""
        if 'revenue' in question.lower():
            if 'region' in question.lower():
                region_revenue = self.df.groupby('Region')['Revenue'].sum()
                lowest_region = region_revenue.idxmin()
                lowest_value = region_revenue.min()
                
                computation = "Summed Revenue by Region and found minimum"
                self.log_computation(question, computation, lowest_value)
                
                return {
                    'answer': f"{lowest_region} region has the lowest total revenue at ${lowest_value:,.0f}",
                    'computation': computation,
                    'supporting_data': {
                        'revenue_by_region': region_revenue.to_dict()
                    }
                }
        
        min_row = self.df.loc[self.df['Revenue'].idxmin()]
        computation = "Found row with minimum Revenue value"
        self.log_computation(question, computation, min_row['Revenue'])
        
        return {
            'answer': f"Lowest revenue record: {min_row['Region']}, {min_row['Quarter']}, {min_row['Product']} with ${min_row['Revenue']:,.0f}",
            'computation': computation,
            'supporting_data': min_row.to_dict()
        }
    
    def _calculate_average(self, question: str) -> Dict[str, Any]:
        """Calculate average values."""
        if 'revenue' in question.lower():
            if 'region' in question.lower():
                avg_revenue = self.df.groupby('Region')['Revenue'].mean().round(0)
                
                computation = "Calculated mean Revenue by Region"
                self.log_computation(question, computation, avg_revenue.to_dict())
                
                return {
                    'answer': f"Average revenue by region: {dict(avg_revenue)}",
                    'computation': computation,
                    'supporting_data': {
                        'average_revenue_by_region': avg_revenue.to_dict()
                    }
                }
            else:
                avg_revenue = self.df['Revenue'].mean()
                
                computation = "Calculated mean of Revenue column"
                self.log_computation(question, computation, avg_revenue)
                
                return {
                    'answer': f"Average revenue across all records: ${avg_revenue:,.0f}",
                    'computation': computation,
                    'supporting_data': {
                        'average_revenue': avg_revenue
                    }
                }
        
        if 'profit' in question.lower():
            avg_profit = self.df['Profit_Margin'].mean()
            
            computation = "Calculated mean of Profit_Margin column"
            self.log_computation(question, computation, avg_profit)
            
            return {
                'answer': f"Average profit margin: {avg_profit:.2%}",
                'computation': computation,
                'supporting_data': {
                    'average_profit_margin': avg_profit
                }
            }
    
    def _calculate_total(self, question: str) -> Dict[str, Any]:
        """Calculate total values."""
        if 'revenue' in question.lower():
            total_revenue = self.df['Revenue'].sum()
            
            computation = "Summed all values in Revenue column"
            self.log_computation(question, computation, total_revenue)
            
            return {
                'answer': f"Total revenue across all regions: ${total_revenue:,.0f}",
                'computation': computation,
                'supporting_data': {
                    'total_revenue': total_revenue
                }
            }
        
        if 'units' in question.lower():
            total_units = self.df['Units_Sold'].sum()
            
            computation = "Summed all values in Units_Sold column"
            self.log_computation(question, computation, total_units)
            
            return {
                'answer': f"Total units sold across all regions: {total_units:,.0f}",
                'computation': computation,
                'supporting_data': {
                    'total_units_sold': total_units
                }
            }
    
    def _compare_values(self, question: str) -> Dict[str, Any]:
        """Compare values between groups."""
        # Extract regions to compare
        regions = [r.capitalize() for r in ['north', 'south', 'east', 'west'] if r in question.lower()]
        
        if len(regions) >= 2:
            region_revenue = self.df.groupby('Region')['Revenue'].sum()
            comparison = {r: region_revenue[r] for r in regions}
            
            computation = f"Summed Revenue by Region and compared {regions}"
            self.log_computation(question, computation, comparison)
            
            return {
                'answer': f"Revenue comparison: {comparison}",
                'computation': computation,
                'supporting_data': comparison
            }
        
        return self._general_query(question)
    
    def _analyze_profit(self, question: str) -> Dict[str, Any]:
        """Analyze profit metrics."""
        if 'highest' in question.lower():
            max_profit = self.df.loc[self.df['Profit_Margin'].idxmax()]
            
            computation = "Found row with maximum Profit_Margin"
            self.log_computation(question, computation, max_profit['Profit_Margin'])
            
            return {
                'answer': f"Highest profit margin: {max_profit['Region']}, {max_profit['Product']} in {max_profit['Quarter']} with {max_profit['Profit_Margin']:.2%}",
                'computation': computation,
                'supporting_data': max_profit.to_dict()
            }
        
        if 'by region' in question.lower():
            avg_profit = self.df.groupby('Region')['Profit_Margin'].mean()
            
            computation = "Calculated mean Profit_Margin by Region"
            self.log_computation(question, computation, avg_profit.to_dict())
            
            return {
                'answer': f"Average profit margin by region: {dict(avg_profit)}",
                'computation': computation,
                'supporting_data': {
                    'profit_margin_by_region': avg_profit.to_dict()
                }
            }
        
        total_profit = (self.df['Revenue'] * self.df['Profit_Margin']).sum()
        
        computation = "Calculated total profit: Sum(Revenue * Profit_Margin)"
        self.log_computation(question, computation, total_profit)
        
        return {
            'answer': f"Total profit across all operations: ${total_profit:,.0f}",
            'computation': computation,
            'supporting_data': {
                'total_profit': total_profit
            }
        }
    
    def _analyze_satisfaction(self, question: str) -> Dict[str, Any]:
        """Analyze customer satisfaction metrics."""
        question_lower = question.lower()
        
        try:
            if 'highest' in question_lower:
                max_sat = self.df.loc[self.df['Customer_Satisfaction'].idxmax()]
                
                computation = "Found row with maximum Customer_Satisfaction"
                self.log_computation(question, computation, max_sat['Customer_Satisfaction'])
                
                return {
                    'answer': f"Highest customer satisfaction: {max_sat['Region']}, {max_sat['Product']} in {max_sat['Quarter']} with {max_sat['Customer_Satisfaction']:.1f}/5.0",
                    'computation': computation,
                    'supporting_data': max_sat.to_dict()
                }
            
            if 'by region' in question_lower:
                avg_sat = self.df.groupby('Region')['Customer_Satisfaction'].mean()
                
                computation = "Calculated mean Customer_Satisfaction by Region"
                self.log_computation(question, computation, avg_sat.to_dict())
                
                return {
                    'answer': f"Average customer satisfaction by region: {dict(avg_sat.round(2))}",
                    'computation': computation,
                    'supporting_data': {
                        'satisfaction_by_region': avg_sat.to_dict()
                    }
                }
            
            avg_sat = self.df['Customer_Satisfaction'].mean()
            
            computation = "Calculated mean of Customer_Satisfaction column"
            self.log_computation(question, computation, avg_sat)
            
            return {
                'answer': f"Average customer satisfaction: {avg_sat:.2f}/5.0",
                'computation': computation,
                'supporting_data': {
                    'average_satisfaction': avg_sat
                }
            }
        except Exception as e:
            return {
                'answer': f"Error analyzing satisfaction: {str(e)}",
                'computation': f"Error in satisfaction analysis: {str(e)}",
                'supporting_data': {}
            }
    
    def _find_best(self, question: str) -> Dict[str, Any]:
        """Find best performing entity."""
        if 'product' in question.lower():
            product_revenue = self.df.groupby('Product')['Revenue'].sum()
            best_product = product_revenue.idxmax()
            
            computation = "Summed Revenue by Product and found maximum"
            self.log_computation(question, computation, best_product)
            
            return {
                'answer': f"Best performing product by revenue: {best_product}",
                'computation': computation,
                'supporting_data': {
                    'revenue_by_product': product_revenue.to_dict()
                }
            }
        
        if 'region' in question.lower():
            region_revenue = self.df.groupby('Region')['Revenue'].sum()
            best_region = region_revenue.idxmax()
            
            computation = "Summed Revenue by Region and found maximum"
            self.log_computation(question, computation, best_region)
            
            return {
                'answer': f"Best performing region by revenue: {best_region}",
                'computation': computation,
                'supporting_data': {
                    'revenue_by_region': region_revenue.to_dict()
                }
            }
        
        return self._general_query(question)
    
    def _find_worst(self, question: str) -> Dict[str, Any]:
        """Find worst performing entity."""
        if 'product' in question.lower():
            product_revenue = self.df.groupby('Product')['Revenue'].sum()
            worst_product = product_revenue.idxmin()
            
            computation = "Summed Revenue by Product and found minimum"
            self.log_computation(question, computation, worst_product)
            
            return {
                'answer': f"Worst performing product by revenue: {worst_product}",
                'computation': computation,
                'supporting_data': {
                    'revenue_by_product': product_revenue.to_dict()
                }
            }
        
        if 'region' in question.lower():
            region_revenue = self.df.groupby('Region')['Revenue'].sum()
            worst_region = region_revenue.idxmin()
            
            computation = "Summed Revenue by Region and found minimum"
            self.log_computation(question, computation, worst_region)
            
            return {
                'answer': f"Worst performing region by revenue: {worst_region}",
                'computation': computation,
                'supporting_data': {
                    'revenue_by_region': region_revenue.to_dict()
                }
            }
        
        return self._general_query(question)
    
    def _general_query(self, question: str) -> Dict[str, Any]:
        """Handle general queries with basic statistics."""
        computation = "Provided general dataset statistics"
        self.log_computation(question, computation, "See supporting data")
        
        return {
            'answer': f"General statistics for your query. See supporting data for details.",
            'computation': computation,
            'supporting_data': {
                'total_records': len(self.df),
                'total_revenue': self.df['Revenue'].sum(),
                'total_units': self.df['Units_Sold'].sum(),
                'average_profit_margin': self.df['Profit_Margin'].mean(),
                'average_satisfaction': self.df['Customer_Satisfaction'].mean()
            }
        }
    
    def get_computation_log(self) -> List[Dict[str, Any]]:
        """Return the log of all computations performed."""
        return self.computation_log
    
    def export_computation_log(self, filename: str):
        """Export computation log to a file."""
        import json
        with open(filename, 'w') as f:
            json.dump(self.computation_log, f, indent=2)


if __name__ == "__main__":
    # Example usage
    agent = DataQAAgent("sample_sales_data.csv")
    
    # Print data info
    print("Dataset Info:")
    print(agent.get_data_info())
    print("\n" + "="*50 + "\n")
    
    # Sample questions
    questions = [
        "Which region grew fastest last quarter?",
        "What is the total revenue across all regions?",
        "Which product has the highest revenue?",
        "What is the average profit margin by region?",
        "Which region has the lowest total revenue?",
        "What is the total units sold?",
        "Which product has the highest profit margin?",
        "What is the average customer satisfaction by region?",
        "Compare revenue between North and South regions",
        "Which is the best performing region?"
    ]
    
    for question in questions:
        print(f"Question: {question}")
        result = agent.answer_question(question)
        print(f"Answer: {result['answer']}")
        print(f"Computation: {result['computation']}")
        print(f"Supporting Data: {result['supporting_data']}")
        print("-" * 50)
