/**
 * ============================================================================
 * STOCK BUY/SELL ANALYZER - Header File
 * ============================================================================
 * A comprehensive C++ application for analyzing stock prices and determining
 * the optimal buy/sell days for maximum profit using efficient O(n) algorithm.
 *
 * Author: College Project
 * Date: February 2026
 * ============================================================================
 */

#ifndef STOCK_ANALYZER_H
#define STOCK_ANALYZER_H

#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <iomanip>
#include <ctime>
#include <limits>

using namespace std;

// ============================================================================
// Data Structure for Analysis Result
// ============================================================================
struct AnalysisResult {
    int buyDay;           // Day index to buy (0-based)
    int sellDay;          // Day index to sell (0-based)
    double buyPrice;      // Price at buy day
    double sellPrice;     // Price at sell day
    double maxProfit;     // Maximum profit achievable
    bool profitPossible;  // True if profit is possible
    string analysisDate;  // Date and time of analysis
};

// ============================================================================
// Function Prototypes
// ============================================================================

// Display Functions
void displayHeader();
void displayMenu();
void displayFooter();
void displayStockPrices(const vector<double>& prices);
void displayAnalysisResult(const AnalysisResult& result);
void displayDashboard(const vector<double>& prices, const AnalysisResult& result);

// Input Functions
void inputStockPrices(vector<double>& prices);
void addStockPrice(vector<double>& prices);
void clearStockPrices(vector<double>& prices);

// Algorithm Functions
AnalysisResult calculateMaxProfit(const vector<double>& prices);

// File Handling Functions
bool saveToCSV(const vector<double>& prices, const AnalysisResult& result, const string& filename);
bool fileExists(const string& filename);
string generateDefaultFilename();

// Utility Functions
void pauseScreen();
void clearScreen();
string getCurrentDateTime();
double calculatePercentageChange(double buyPrice, double sellPrice);

#endif // STOCK_ANALYZER_H
