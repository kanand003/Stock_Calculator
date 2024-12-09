import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

class RetailInvestorStockAnalyzer:
    @staticmethod
    def get_key_metrics(ticker):
        """
        Get simple, essential metrics for a retail investor
        
        :param ticker: Stock ticker symbol
        :return: Dictionary of key metrics
        """
        try:
            # Fetch stock data
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Basic Fundamental Metrics
            metrics = {
                # Valuation Metrics
                "Valuation": {
                    "Current Price": f"₹{info.get('currentPrice', 'N/A'):.2f}",
                    "Market Cap": f"₹{info.get('marketCap', 'N/A'):,}",
                    "P/E Ratio": round(info.get('trailingPE', 0), 2),
                    "Price to Book": round(info.get('priceToBook', 0), 2),
                    "Forward P/E": round(info.get('forwardPE', 0), 2)
                },
                
                # Dividend Metrics
                "Dividend": {
                    "Dividend Yield": f"{info.get('dividendYield', 0)*100:.2f}%",
                    "Dividend Rate": f"₹{info.get('dividendRate', 'N/A'):.2f}",
                    "Payout Ratio": f"{info.get('payoutRatio', 0)*100:.2f}%"
                },
                
                # Performance Metrics
                "Performance": {
                    "52-Week High": f"₹{info.get('fiftyTwoWeekHigh', 'N/A'):.2f}",
                    "52-Week Low": f"₹{info.get('fiftyTwoWeekLow', 'N/A'):.2f}",
                    "1Y Return": f"{info.get('52WeekChange', 0)*100:.2f}%"
                },
                
                # Growth Metrics
                "Growth": {
                    "EPS (Trailing)": round(info.get('trailingEps', 0), 2),
                    "EPS (Forward)": round(info.get('forwardEps', 0), 2),
                    "Revenue Growth": f"{info.get('revenueGrowth', 0)*100:.2f}%"
                }
            }
            
            return metrics
        
        except Exception as e:
            st.error(f"Error fetching stock data: {e}")
            return None
    
    @staticmethod
    def plot_price_history(ticker, period='1y'):
        """
        Create price history chart
        
        :param ticker: Stock ticker symbol
        :param period: Time period for historical data
        :return: Plotly figure
        """
        try:
            # Download historical data
            df = yf.download(ticker, period=period)
            
            # Create line chart
            fig = go.Figure(data=[
                go.Scatter(
                    x=df.index, 
                    y=df['Close'], 
                    mode='lines', 
                    name='Closing Price',
                    line=dict(color='blue', width=2)
                )
            ])
            
            fig.update_layout(
                title=f'{ticker} Stock Price History',
                xaxis_title='Date',
                yaxis_title='Price (₹)',
                template='plotly_white'
            )
            
            return fig
        
        except Exception as e:
            st.error(f"Error creating stock chart: {e}")
            return None

def main():
    st.set_page_config(page_title="Retail Investor Stock Analyzer", page_icon="💹", layout="wide")
    
    st.title("🚀 Retail Investor Stock Analysis Tool")
    st.write("Simple, essential metrics for individual investors")
    
    # Stock ticker input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        ticker = st.text_input("Enter Stock Ticker", placeholder="e.g. INFY.NS, RELIANCE.NS")
    
    with col2:
        st.write("") # Spacing
        analyze_button = st.button("Analyze Stock")
    
    # Analyze stock
    if ticker or analyze_button:
        # Fetch metrics
        metrics = RetailInvestorStockAnalyzer.get_key_metrics(ticker)
        
        if metrics:
            # Display company name
            stock = yf.Ticker(ticker)
            st.header(f"📊 {stock.info.get('longName', ticker)}")
            
            # Create tabs for different metric categories
            tabs = st.tabs(list(metrics.keys()))
            
            # Display metrics in tabs
            for i, (category, category_metrics) in enumerate(metrics.items()):
                with tabs[i]:
                    # Create columns to display metrics
                    cols = st.columns(3)
                    
                    # Flatten and display metrics
                    flat_metrics = list(category_metrics.items())
                    
                    for j, (name, value) in enumerate(flat_metrics):
                        with cols[j % 3]:
                            st.metric(name, value)
            
            # Stock Price History Chart
            st.header("Stock Price History")
            price_history = RetailInvestorStockAnalyzer.plot_price_history(ticker)
            
            if price_history:
                st.plotly_chart(price_history, use_container_width=True)
            
            # Additional Insights
            st.header("Quick Insights")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("🔍 **Valuation Indicator**")
                pe_ratio = metrics['Valuation']['P/E Ratio']
                if pe_ratio < 15:
                    st.success("Low P/E - Potentially Undervalued")
                elif pe_ratio > 25:
                    st.warning("High P/E - Potentially Overvalued")
                else:
                    st.info("Reasonable Valuation")
            
            with col2:
                st.write("💰 **Dividend Health**")
                dividend_yield = float(metrics['Dividend']['Dividend Yield'].replace('%', ''))
                if dividend_yield > 3:
                    st.success("High Dividend Yield")
                elif dividend_yield > 1:
                    st.info("Moderate Dividend")
                else:
                    st.warning("Low Dividend Yield")
            
            with col3:
                st.write("📈 **Growth Potential**")
                revenue_growth = float(metrics['Growth']['Revenue Growth'].replace('%', ''))
                if revenue_growth > 10:
                    st.success("Strong Growth Potential")
                elif revenue_growth > 5:
                    st.info("Moderate Growth")
                else:
                    st.warning("Limited Growth")

if __name__ == "__main__":
    main()

# Requirements:
# streamlit
# yfinance
# pandas
# plotly
"""
Key Metrics for Retail Investors:

1. Valuation Metrics
   - Current Price
   - Market Cap
   - P/E Ratio (Price to Earnings)
   - Price to Book
   - Forward P/E

2. Dividend Metrics
   - Dividend Yield
   - Dividend Rate
   - Payout Ratio

3. Performance Metrics
   - 52-Week High/Low
   - 1-Year Return

4. Growth Metrics
   - Earnings Per Share (EPS)
   - Revenue Growth

Additional Features:
- Simple, color-coded insights
- Price history chart
- Easy-to-understand metric categories
"""