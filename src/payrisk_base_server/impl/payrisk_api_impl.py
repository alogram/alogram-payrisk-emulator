# coding: utf-8
import logging
import time
from typing import Optional, Dict, Any

from payrisk_base_server.apis.payrisk_api_base import BasePayriskApi
from payrisk_base_server.models.check_request import CheckRequest
from payrisk_base_server.models.decision_response import DecisionResponse
from payrisk_base_server.models.fraud_score import FraudScore
from payrisk_base_server.models.scores_success_response import ScoresSuccessResponse
from payrisk_base_server.models.risk_breakdown import RiskBreakdown
from payrisk_base_server.models.category_signal import CategorySignal

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("alogram.payrisk.emulator")


class PayriskApiImpl(BasePayriskApi):
    async def risk_check(
        self,
        x_idempotency_key: str,
        check_request: CheckRequest,
        x_trace_id: Optional[str] = None,
    ) -> DecisionResponse:
        logger.info(
            f"🔍 RECEIVED RISK CHECK | IdempotencyKey: {x_idempotency_key} | TraceId: {x_trace_id}"
        )

        # 📱 Phone Intelligence Simulation
        identity = getattr(check_request, "identity", None)
        phone = getattr(identity, "phone", None) if identity else None
        
        identity_signal = CategorySignal(level="low", score=0.01)
        
        if phone:
            logger.info(f"📱 Processing Phone Intelligence for: ***{str(phone)[-4:]}")
            # Simulate different forensics based on phone number suffix
            if phone.endswith("666"):  # 🚨 High Risk / Spam
                identity_signal = CategorySignal(
                    level="high", 
                    score=0.85, 
                    reasons=["PHONE_SPAM_REGISTRY_MATCH"],
                    # metadata will be added once models are regenerated
                )
            elif phone.endswith("999"):  # ⚠️ Synergy Risk (VOIP + Spam)
                identity_signal = CategorySignal(
                    level="critical", 
                    score=0.99, 
                    reasons=["PHONE_FORENSIC_SYNERGY_CRITICAL"]
                )
            else:  # ✅ Clean Number
                identity_signal = CategorySignal(level="low", score=0.0)

        # Return a standard "approve" decision for the emulator
        decision = DecisionResponse(
            assessment_id=f"ast_{x_idempotency_key.split('_')[-1]}",
            decision="approve" if identity_signal.level != "critical" else "decline",
            score=FraudScore(score=identity_signal.score or 0.01, label=identity_signal.level),
            risk_level=identity_signal.level,
            decision_score=identity_signal.score or 0.01,
            decision_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            breakdown=RiskBreakdown(identity=identity_signal)
        )

        logger.info(
            f"✅ EMITTED DECISION | IdempotencyKey: {x_idempotency_key} | Decision: {decision.decision} | Risk: {decision.risk_level}"
        )
        return decision

    async def ingest_payment_event(
        self, x_idempotency_key, payment_event, x_trace_id
    ) -> None:
        logger.info(
            f"📥 INGESTED EVENT | IdempotencyKey: {x_idempotency_key} | Type: {payment_event.event_type}"
        )
        return None

    async def ingest_signals(
        self, x_idempotency_key, signals_request, x_trace_id
    ) -> None:
        logger.info(
            f"📡 INGESTED SIGNALS | IdempotencyKey: {x_idempotency_key} | Count: {len(signals_request.signals)}"
        )
        return None

    async def get_fraud_scores(
        self,
        tenantId,
        x_trace_id,
        x_idempotency_key,
        start_time,
        end_time,
        page_size,
        page_token,
    ) -> ScoresSuccessResponse:
        logger.info(f"📊 FETCHED FRAUD SCORES | Tenant: {tenantId}")
        return ScoresSuccessResponse(scores=[])

    async def health_check(self) -> None:
        return None

    async def account_risk_check(
        self, x_idempotency_key, account_check_request, x_trace_id
    ) -> DecisionResponse:
        logger.info(f"👤 ACCOUNT RISK CHECK | IdempotencyKey: {x_idempotency_key}")
        return await self.risk_check(x_idempotency_key, None, x_trace_id)

    async def kyc_risk_check(
        self, x_idempotency_key, kyc_check_request, x_trace_id
    ) -> DecisionResponse:
        logger.info(f"🆔 KYC RISK CHECK | IdempotencyKey: {x_idempotency_key}")
        return await self.risk_check(x_idempotency_key, None, x_trace_id)
