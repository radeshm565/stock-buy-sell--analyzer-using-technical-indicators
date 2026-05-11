/**
 * ============================================================================
 * STOCK BUY/SELL ANALYZER - Main Application
 * ============================================================================
 * A comprehensive C++ application for analyzing stock prices and determining
 * the optimal buy/sell days for maximum profit.
 *
 * FEATURES:
 * - Manual input of stock prices using std::vector
 * - Efficient O(n) algorithm for maximum profit calculation
 * - Menu-driven console interface with dashboard-style output
 * - CSV file export for analysis results
 * - Modular design with separate header and implementation files
 *
 * ALGORITHM:
 * Uses Kadane's algorithm approach (modified) for single transaction:
 * - Time Complexity: O(n) - Single pass through price array
 * - Space Complexity: O(1) - Constant extra space
 *
 * Author: College Project
 * Course: Data Structures and Algorithms
 * Date: February 2026
 * ============================================================================
 */

#include "stock_analyzer.h"

// ============================================================================
// MAIN FUNCTION
// ============================================================================

int main() {
    // Vector to store stock prices dynamically
    vector<double> stockPrices;

    // Structure to store analysis results
    AnalysisResult analysisResult;
    analysisResult.profitPossible = false;

    int choice;
    bool running = true;

    // Clear screen and display welcome header
    clearScreen();
    displayHeader();

    cout << "Welcome to Stock Buy/Sell Analyzer!\n";
    cout << "This application helps you find the best days to buy and sell\n";
    cout << "stocks for maximum profit using an efficient O(n) algorithm.\n";

    pauseScreen();

    // Main application loop
    while (running) {
        clearScreen();
        displayHeader();
        displayMenu();

        // Get user choice with input validation
        while (!(cin >> choice)) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "\n❌ Invalid input. Please enter a number (0-7): ";
        }

        // Process user choice
        switch (choice) {
            case 1: {
                // Option 1: Manual Input of Stock Prices
                clearScreen();
                displayHeader();
                inputStockPrices(stockPrices);

                // Automatically calculate analysis for new data
                if (!stockPrices.empty()) {
                    analysisResult = calculateMaxProfit(stockPrices);
                }

                pauseScreen();
                break;
            }

            case 2: {
                // Option 2: Add Single Stock Price
                clearScreen();
                displayHeader();
                addStockPrice(stockPrices);

                // Recalculate analysis with new price
                if (!stockPrices.empty()) {
                    analysisResult = calculateMaxProfit(stockPrices);
                }

                pauseScreen();
                break;
            }

            case 3: {
                // Option 3: Display Current Stock Prices
                clearScreen();
                displayHeader();
                displayStockPrices(stockPrices);
                pauseScreen();
                break;
            }

            case 4: {
                // Option 4: Calculate Maximum Profit
                clearScreen();
                displayHeader();

                if (stockPrices.empty()) {
                    cout << "\n⚠️  No stock prices available. Please add prices first.\n";
                } else if (stockPrices.size() < 2) {
                    cout << "\n⚠️  At least 2 days of prices required for profit calculation.\n";
                } else {
                    analysisResult = calculateMaxProfit(stockPrices);
                    displayAnalysisResult(analysisResult);
                }

                pauseScreen();
                break;
            }

            case 5: {
                // Option 5: Show Analysis Dashboard
                if (!stockPrices.empty()) {
                    analysisResult = calculateMaxProfit(stockPrices);
                }
                displayDashboard(stockPrices, analysisResult);
                pauseScreen();
                break;
            }

            case 6: {
                // Option 6: Save Analysis to CSV File
                clearScreen();
                displayHeader();

                if (stockPrices.empty()) {
                    cout << "\n⚠️  No stock prices available. Please add prices first.\n";
                    pauseScreen();
                    break;
                }

                // Ensure analysis is up to date
                analysisResult = calculateMaxProfit(stockPrices);

                cout << "\n";
                cout << "┌─────────────────────────────────────────────────────────────────────────┐\n";
                cout << "│                 💾 SAVE ANALYSIS TO CSV                                 │\n";
                cout << "└─────────────────────────────────────────────────────────────────────────┘\n";

                cout << "\nOptions:\n";
                cout << "[1] Use default filename (stock_analysis_YYYYMMDD_HHMMSS.csv)\n";
                cout << "[2] Enter custom filename\n";
                cout << "\n👉 Enter your choice: ";

                int saveChoice;
                while (!(cin >> saveChoice) || (saveChoice != 1 && saveChoice != 2)) {
                    cin.clear();
                    cin.ignore(numeric_limits<streamsize>::max(), '\n');
                    cout << "❌ Invalid choice. Enter 1 or 2: ";
                }

                string filename;
                if (saveChoice == 1) {
                    filename = generateDefaultFilename();
                } else {
                    cout << "\nEnter filename (with .csv extension): ";
                    cin >> filename;
                }

                // Check if file already exists
                if (fileExists(filename)) {
                    cout << "\n⚠️  File '" << filename << "' already exists.\n";
                    cout << "Overwrite? (y/n): ";
                    char confirm;
                    cin >> confirm;
                    if (confirm != 'y' && confirm != 'Y') {
                        cout << "\n❌ Save cancelled.\n";
                        pauseScreen();
                        break;
                    }
                }

                // Save to CSV
                if (saveToCSV(stockPrices, analysisResult, filename)) {
                    cout << "\n✅ Analysis saved successfully to: " << filename << "\n";
                } else {
                    cout << "\n❌ Error saving file. Please check permissions and try again.\n";
                }

                pauseScreen();
                break;
            }

            case 7: {
                // Option 7: Clear All Stock Prices
                clearScreen();
                displayHeader();

                if (stockPrices.empty()) {
                    cout << "\n⚠️  No stock prices to clear.\n";
                } else {
                    cout << "\nAre you sure you want to clear all " << stockPrices.size();
                    cout << " stock prices? (y/n): ";
                    char confirm;
                    cin >> confirm;

                    if (confirm == 'y' || confirm == 'Y') {
                        clearStockPrices(stockPrices);
                        analysisResult.profitPossible = false;
                    } else {
                        cout << "\n❌ Clear operation cancelled.\n";
                    }
                }

                pauseScreen();
                break;
            }

            case 0: {
                // Option 0: Exit Application
                clearScreen();
                displayFooter();
                running = false;
                break;
            }

            default: {
                // Invalid choice
                cout << "\n❌ Invalid choice. Please enter a number between 0 and 7.\n";
                pauseScreen();
                break;
            }
        }
    }

    return 0;
}
