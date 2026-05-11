/**
 * ============================================================================
 * STOCK BUY/SELL ANALYZER - Implementation File
 * ============================================================================
 * Contains all function implementations for the Stock Buy/Sell Analyzer
 * including display functions, input handling, O(n) algorithm, and file I/O.
 * ============================================================================
 */

#include "stock_analyzer.h"

// ============================================================================
// DISPLAY FUNCTIONS
// ============================================================================

/**
 * Displays the application header with title and decorative borders
 */
void displayHeader() {
    cout << "\n";
    cout << "╔══════════════════════════════════════════════════════════════════════════╗\n";
    cout << "║                                                                          ║\n";
    cout << "║           📈  STOCK BUY/SELL ANALYZER  📉                                ║\n";
    cout << "║                                                                          ║\n";
    cout << "║           Maximum Profit Calculator with O(n) Efficiency                 ║\n";
    cout << "║                                                                          ║\n";
    cout << "╚══════════════════════════════════════════════════════════════════════════╝\n";
    cout << "\n";
}

/**
 * Displays the main menu options
 */
void displayMenu() {
    cout << "┌─────────────────────────────────────────────────────────────────────────┐\n";
    cout << "│                         MAIN MENU                                       │\n";
    cout << "├─────────────────────────────────────────────────────────────────────────┤\n";
    cout << "│  [1] 📝 Enter Stock Prices (Manual Input)                               │\n";
    cout << "│  [2] ➕ Add Single Stock Price                                          │\n";
    cout << "│  [3] 📊 Display Current Stock Prices                                    │\n";
    cout << "│  [4] 💰 Calculate Maximum Profit                                        │\n";
    cout << "│  [5] 📈 Show Analysis Dashboard                                         │\n";
    cout << "│  [6] 💾 Save Analysis to CSV File                                       │\n";
    cout << "│  [7] 🗑️  Clear All Stock Prices                                         │\n";
    cout << "│  [0] 🚪 Exit Application                                                │\n";
    cout << "└─────────────────────────────────────────────────────────────────────────┘\n";
    cout << "\n👉 Enter your choice: ";
}

/**
 * Displays the application footer
 */
void displayFooter() {
    cout << "\n";
    cout << "═══════════════════════════════════════════════════════════════════════════\n";
    cout << "                    Thank you for using Stock Analyzer!                    \n";
    cout << "═══════════════════════════════════════════════════════════════════════════\n";
    cout << "\n";
}

/**
 * Displays all stock prices in a formatted table
 * @param prices Vector containing stock prices
 */
void displayStockPrices(const vector<double>& prices) {
    if (prices.empty()) {
        cout << "\n⚠️  No stock prices available. Please add prices first.\n";
        return;
    }

    cout << "\n";
    cout << "┌─────────────────────────────────────────────────────────────────────────┐\n";
    cout << "│                     📊 STOCK PRICE LIST                                 │\n";
    cout << "├──────────┬──────────────────────────────────────────────────────────────┤\n";
    cout << "│  Day #   │  Price ($)                                                   │\n";
    cout << "├──────────┼──────────────────────────────────────────────────────────────┤\n";

    for (size_t i = 0; i < prices.size(); i++) {
        cout << "│  Day " << setw(3) << (i + 1) << " │  $" << setw(10) << fixed << setprecision(2) << prices[i];
        cout << setw(48) << "│\n";
    }

    cout << "├──────────┴──────────────────────────────────────────────────────────────┤\n";
    cout << "│  Total Days: " << setw(3) << prices.size() << setw(54) << "│\n";
    cout << "└─────────────────────────────────────────────────────────────────────────┘\n";
}

/**
 * Displays the analysis result in a formatted box
 * @param result AnalysisResult structure containing buy/sell information
 */
void displayAnalysisResult(const AnalysisResult& result) {
    cout << "\n";
    cout << "╔══════════════════════════════════════════════════════════════════════════╗\n";
    cout << "║                    💰 PROFIT ANALYSIS RESULT                             ║\n";
    cout << "╠══════════════════════════════════════════════════════════════════════════╣\n";

    if (!result.profitPossible) {
        cout << "║                                                                          ║\n";
        cout << "║     ⚠️  NO PROFIT POSSIBLE                                               ║\n";
        cout << "║                                                                          ║\n";
        cout << "║     Stock prices are in descending order.                                ║\n";
        cout << "║     No profitable transaction possible with single buy/sell.             ║\n";
        cout << "║                                                                          ║\n";
    } else {
        double percentageChange = calculatePercentageChange(result.buyPrice, result.sellPrice);

        cout << "║  ┌──────────────────────────────────────────────────────────────────┐    ║\n";
        cout << "║  │  📅 Analysis Date: " << setw(45) << left << result.analysisDate << "│    ║\n";
        cout << "║  ├──────────────────────────────────────────────────────────────────┤    ║\n";
        cout << "║  │  🛒 BUY  Day: " << setw(4) << (result.buyDay + 1) << "  @  $" << setw(10) << fixed << setprecision(2) << result.buyPrice;
        cout << setw(25) << " " << "│    ║\n";
        cout << "║  │  💵 SELL Day: " << setw(4) << (result.sellDay + 1) << "  @  $" << setw(10) << result.sellPrice;
        cout << setw(25) << " " << "│    ║\n";
        cout << "║  ├──────────────────────────────────────────────────────────────────┤    ║\n";
        cout << "║  │  💰 MAXIMUM PROFIT:     $" << setw(10) << result.maxProfit;
        cout << setw(31) << " " << "│    ║\n";
        cout << "║  │  📈 Return Percentage:  " << setw(6) << fixed << setprecision(2) << percentageChange << "%";
        cout << setw(35) << " " << "│    ║\n";
        cout << "║  └──────────────────────────────────────────────────────────────────┘    ║\n";
    }

    cout << "╚══════════════════════════════════════════════════════════════════════════╝\n";
}

/**
 * Displays a comprehensive dashboard with all information
 * @param prices Vector containing stock prices
 * @param result AnalysisResult structure containing analysis information
 */
void displayDashboard(const vector<double>& prices, const AnalysisResult& result) {
    clearScreen();
    displayHeader();

    // Stock Prices Section
    displayStockPrices(prices);

    // Analysis Section
    if (!prices.empty()) {
        displayAnalysisResult(result);

        // Summary Statistics
        double minPrice = prices[0];
        double maxPrice = prices[0];
        double total = 0;

        for (double price : prices) {
            if (price < minPrice) minPrice = price;
            if (price > maxPrice) maxPrice = price;
            total += price;
        }

        double average = total / prices.size();

        cout << "\n";
        cout << "┌─────────────────────────────────────────────────────────────────────────┐\n";
        cout << "│                     📈 PRICE STATISTICS                                 │\n";
        cout << "├─────────────────────────────────────────────────────────────────────────┤\n";
        cout << "│  Minimum Price:  $" << setw(10) << fixed << setprecision(2) << minPrice;
        cout << setw(40) << "│\n";
        cout << "│  Maximum Price:  $" << setw(10) << maxPrice;
        cout << setw(40) << "│\n";
        cout << "│  Average Price:  $" << setw(10) << average;
        cout << setw(40) << "│\n";
        cout << "└─────────────────────────────────────────────────────────────────────────┘\n";
    }
}

// ============================================================================
// INPUT FUNCTIONS
// ============================================================================

/**
 * Allows user to input multiple stock prices manually
 * @param prices Vector to store the stock prices
 */
void inputStockPrices(vector<double>& prices) {
    int numDays;
    double price;

    cout << "\n";
    cout << "┌─────────────────────────────────────────────────────────────────────────┐\n";
    cout << "│                 📝 MANUAL STOCK PRICE INPUT                             │\n";
    cout << "└─────────────────────────────────────────────────────────────────────────┘\n";

    cout << "\nEnter the number of days: ";
    while (!(cin >> numDays) || numDays <= 0) {
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        cout << "❌ Invalid input. Please enter a positive number: ";
    }

    prices.clear();
    prices.reserve(numDays);

    cout << "\nEnter stock prices for " << numDays << " days:\n";
    cout << "────────────────────────────────────────\n";

    for (int i = 0; i < numDays; i++) {
        cout << "Day " << (i + 1) << " price: $";
        while (!(cin >> price) || price < 0) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "❌ Invalid input. Please enter a non-negative price: $";
        }
        prices.push_back(price);
    }

    cout << "\n✅ Successfully entered " << numDays << " stock prices!\n";
}

/**
 * Adds a single stock price to the existing vector
 * @param prices Vector to add the price to
 */
void addStockPrice(vector<double>& prices) {
    double price;

    cout << "\n";
    cout << "┌─────────────────────────────────────────────────────────────────────────┐\n";
    cout << "│                 ➕ ADD SINGLE STOCK PRICE                               │\n";
    cout << "└─────────────────────────────────────────────────────────────────────────┘\n";

    cout << "\nEnter price for Day " << (prices.size() + 1) << ": $";
    while (!(cin >> price) || price < 0) {
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        cout << "❌ Invalid input. Please enter a non-negative price: $";
    }

    prices.push_back(price);
    cout << "\n✅ Price added successfully! Total days: " << prices.size() << "\n";
}

/**
 * Clears all stock prices from the vector
 * @param prices Vector to clear
 */
void clearStockPrices(vector<double>& prices) {
    prices.clear();
    cout << "\n🗑️  All stock prices have been cleared.\n";
}

// ============================================================================
// ALGORITHM FUNCTIONS
// ============================================================================

/**
 * Calculates the maximum profit using efficient O(n) algorithm
 * This uses Kadane's algorithm approach - single pass through the array
 *
 * Algorithm Explanation:
 * - Track the minimum price seen so far (best day to buy)
 * - For each day, calculate profit if sold on that day
 * - Keep track of maximum profit and corresponding buy/sell days
 * - Time Complexity: O(n) - Single pass through the array
 * - Space Complexity: O(1) - Only using a few variables
 *
 * @param prices Vector containing stock prices
 * @return AnalysisResult structure with buy/sell information
 */
AnalysisResult calculateMaxProfit(const vector<double>& prices) {
    AnalysisResult result;
    result.analysisDate = getCurrentDateTime();

    // Handle edge cases
    if (prices.size() < 2) {
        result.profitPossible = false;
        result.buyDay = -1;
        result.sellDay = -1;
        result.buyPrice = 0;
        result.sellPrice = 0;
        result.maxProfit = 0;
        return result;
    }

    // Initialize with first day
    int minPriceDay = 0;
    double minPrice = prices[0];
    double maxProfit = 0;
    int bestBuyDay = 0;
    int bestSellDay = 0;

    // O(n) algorithm - Single pass through prices
    for (size_t i = 1; i < prices.size(); i++) {
        // Update minimum price if current price is lower
        if (prices[i] < minPrice) {
            minPrice = prices[i];
            minPriceDay = i;
        }

        // Calculate profit if we sell on current day
        double currentProfit = prices[i] - minPrice;

        // Update maximum profit if current profit is better
        if (currentProfit > maxProfit) {
            maxProfit = currentProfit;
            bestBuyDay = minPriceDay;
            bestSellDay = i;
        }
    }

    // Populate result structure
    result.buyDay = bestBuyDay;
    result.sellDay = bestSellDay;
    result.buyPrice = prices[bestBuyDay];
    result.sellPrice = prices[bestSellDay];
    result.maxProfit = maxProfit;
    result.profitPossible = (maxProfit > 0);

    return result;
}

// ============================================================================
// FILE HANDLING FUNCTIONS
// ============================================================================

/**
 * Saves the analysis results to a CSV file
 * @param prices Vector containing stock prices
 * @param result AnalysisResult structure containing analysis information
 * @param filename Name of the file to save to
 * @return true if successful, false otherwise
 */
bool saveToCSV(const vector<double>& prices, const AnalysisResult& result, const string& filename) {
    ofstream file(filename);

    if (!file.is_open()) {
        return false;
    }

    // Write CSV header
    file << "Stock Buy/Sell Analyzer - Analysis Report\n";
    file << "Generated on," << result.analysisDate << "\n";
    file << "\n";

    // Write stock prices
    file << "Day Number,Stock Price\n";
    for (size_t i = 0; i < prices.size(); i++) {
        file << (i + 1) << "," << fixed << setprecision(2) << prices[i] << "\n";
    }

    file << "\n";
    file << "Analysis Results\n";
    file << "Metric,Value\n";

    if (result.profitPossible) {
        file << "Buy Day," << (result.buyDay + 1) << "\n";
        file << "Buy Price,$" << fixed << setprecision(2) << result.buyPrice << "\n";
        file << "Sell Day," << (result.sellDay + 1) << "\n";
        file << "Sell Price,$" << fixed << setprecision(2) << result.sellPrice << "\n";
        file << "Maximum Profit,$" << fixed << setprecision(2) << result.maxProfit << "\n";
        file << "Return Percentage," << fixed << setprecision(2);
        file << calculatePercentageChange(result.buyPrice, result.sellPrice) << "%\n";
    } else {
        file << "Result,No profit possible\n";
        file << "Reason,Stock prices are in descending order\n";
    }

    file.close();
    return true;
}

/**
 * Checks if a file already exists
 * @param filename Name of the file to check
 * @return true if file exists, false otherwise
 */
bool fileExists(const string& filename) {
    ifstream file(filename);
    return file.good();
}

/**
 * Generates a default filename based on current date and time
 * @return Generated filename string
 */
string generateDefaultFilename() {
    time_t now = time(0);
    tm* ltm = localtime(&now);

    char buffer[50];
    sprintf(buffer, "stock_analysis_%04d%02d%02d_%02d%02d%02d.csv",
            1900 + ltm->tm_year, 1 + ltm->tm_mon, ltm->tm_mday,
            ltm->tm_hour, ltm->tm_min, ltm->tm_sec);

    return string(buffer);
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Pauses the screen and waits for user to press Enter
 */
void pauseScreen() {
    cout << "\n";
    cout << "Press Enter to continue...";
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    cin.get();
}

/**
 * Clears the console screen (cross-platform)
 */
void clearScreen() {
    #ifdef _WIN32
        system("cls");
    #else
        system("clear");
    #endif
}

/**
 * Gets the current date and time as a formatted string
 * @return Formatted date-time string
 */
string getCurrentDateTime() {
    time_t now = time(0);
    tm* ltm = localtime(&now);

    char buffer[30];
    sprintf(buffer, "%04d-%02d-%02d %02d:%02d:%02d",
            1900 + ltm->tm_year, 1 + ltm->tm_mon, ltm->tm_mday,
            ltm->tm_hour, ltm->tm_min, ltm->tm_sec);

    return string(buffer);
}

/**
 * Calculates the percentage change between buy and sell prices
 * @param buyPrice Price at which stock was bought
 * @param sellPrice Price at which stock was sold
 * @return Percentage change
 */
double calculatePercentageChange(double buyPrice, double sellPrice) {
    if (buyPrice == 0) return 0;
    return ((sellPrice - buyPrice) / buyPrice) * 100;
}
