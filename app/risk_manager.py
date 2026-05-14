MAX_POSITION_USD = 1000
MAX_DAILY_LOSS_PCT = -0.05
MAX_CONCENTRATION_PCT = 0.25
OPTIMAL_CONCENTRATION_PCT = 0.10

class RiskManager:
    def __init__(self, portfolio_value: float):
        self.portfolio_value = portfolio_value

    def max_position_size(self) -> float:
        return min(MAX_POSITION_USD, self.portfolio_value * MAX_CONCENTRATION_PCT)

    def optimal_position_size(self) -> float:
        return min(MAX_POSITION_USD, self.portfolio_value * OPTIMAL_CONCENTRATION_PCT)

    def within_concentration(self, position_value: float) -> bool:
        return position_value <= self.portfolio_value * MAX_CONCENTRATION_PCT

    def should_stop_loss(self, pnl_pct: float) -> bool:
        return pnl_pct <= -0.02

    def daily_loss_limit_hit(self, daily_pnl_pct: float) -> bool:
        return daily_pnl_pct <= MAX_DAILY_LOSS_PCT

    def allocation_for_order(self, price: float) -> int:
        if price <= 0:
            return 0
        allocation = self.max_position_size()
        return int(allocation // price)
