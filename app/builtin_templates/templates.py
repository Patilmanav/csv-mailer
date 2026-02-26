"""Built-in HTML email templates with plain-text fallbacks."""

TEMPLATES = {
    "welcome": {
        "name": "Welcome Email",
        "description": "Warm onboarding email for new users or customers",
        "subject": "Welcome, {{name}}! 🎉",
        "html": """<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f4f6fb;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f6fb;padding:40px 0;">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.07);">
        <!-- Header -->
        <tr><td style="background:linear-gradient(135deg,#6366f1,#7c3aed);padding:40px 48px;text-align:center;">
          <h1 style="color:#ffffff;margin:0;font-size:28px;font-weight:700;letter-spacing:-0.5px;">Welcome aboard! 🎉</h1>
          <p style="color:rgba(255,255,255,0.85);margin:10px 0 0;font-size:15px;">We're thrilled to have you with us.</p>
        </td></tr>
        <!-- Body -->
        <tr><td style="padding:40px 48px;">
          <p style="color:#374151;font-size:16px;line-height:1.6;margin:0 0 20px;">Hi <strong>{{name}}</strong>,</p>
          <p style="color:#374151;font-size:15px;line-height:1.7;margin:0 0 24px;">
            Thank you for joining <strong>{{company}}</strong>. Your account is ready and we can't wait to show you everything we have in store.
          </p>
          <div style="text-align:center;margin:32px 0;">
            <a href="#" style="background:linear-gradient(135deg,#6366f1,#7c3aed);color:#ffffff;text-decoration:none;padding:14px 36px;border-radius:8px;font-size:15px;font-weight:600;display:inline-block;">Get Started →</a>
          </div>
          <p style="color:#6b7280;font-size:14px;line-height:1.6;margin:0;">If you have any questions, just reply to this email — we're always happy to help.</p>
        </td></tr>
        <!-- Footer -->
        <tr><td style="background:#f9fafb;padding:24px 48px;text-align:center;border-top:1px solid #e5e7eb;">
          <p style="color:#9ca3af;font-size:12px;margin:0;">© 2025 {{company}} · You received this because you signed up.</p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>""",
        "plaintext": """Hi {{name}},

Welcome to {{company}}! We're thrilled to have you on board.

Your account is ready. Get started by visiting our website.

If you have any questions, just reply to this email — we're always happy to help.

© 2025 {{company}}"""
    },

    "newsletter": {
        "name": "Newsletter",
        "description": "Clean newsletter layout with a hero section and article blocks",
        "subject": "{{month}} Newsletter — {{headline}}",
        "html": """<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f1f5f9;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f1f5f9;padding:40px 0;">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:12px;overflow:hidden;">
        <!-- Banner -->
        <tr><td style="background:#0f172a;padding:28px 48px;text-align:center;">
          <p style="color:#a78bfa;font-size:12px;font-weight:700;letter-spacing:2px;margin:0 0 6px;text-transform:uppercase;">Monthly Newsletter</p>
          <h1 style="color:#ffffff;font-size:24px;margin:0;font-weight:700;">{{headline}}</h1>
        </td></tr>
        <!-- Greeting -->
        <tr><td style="padding:36px 48px 0;">
          <p style="color:#374151;font-size:15px;line-height:1.7;margin:0;">Hi {{name}}, here's what's new this {{month}}:</p>
        </td></tr>
        <!-- Article 1 -->
        <tr><td style="padding:28px 48px 0;">
          <div style="border-left:4px solid #6366f1;padding-left:16px;">
            <p style="color:#6366f1;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin:0 0 6px;">Feature</p>
            <h2 style="color:#111827;font-size:17px;margin:0 0 8px;font-weight:700;">{{feature_title}}</h2>
            <p style="color:#6b7280;font-size:14px;line-height:1.7;margin:0;">{{feature_body}}</p>
          </div>
        </td></tr>
        <!-- Divider -->
        <tr><td style="padding:24px 48px;"><hr style="border:none;border-top:1px solid #e5e7eb;"></td></tr>
        <!-- CTA -->
        <tr><td style="padding:0 48px 36px;text-align:center;">
          <a href="#" style="background:#6366f1;color:#fff;text-decoration:none;padding:13px 32px;border-radius:8px;font-size:14px;font-weight:600;display:inline-block;">Read Full Newsletter →</a>
        </td></tr>
        <!-- Footer -->
        <tr><td style="background:#f8fafc;padding:20px 48px;text-align:center;border-top:1px solid #e5e7eb;">
          <p style="color:#94a3b8;font-size:12px;margin:0;">{{company}} · <a href="#" style="color:#94a3b8;">Unsubscribe</a></p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>""",
        "plaintext": """Hi {{name}},

Here's what's new this {{month}}:

FEATURE: {{feature_title}}
{{feature_body}}

Read the full newsletter on our website.

---
{{company}} | To unsubscribe, reply with "unsubscribe"."""
    },

    "invoice": {
        "name": "Invoice / Payment",
        "description": "Professional invoice notification with amount and due date",
        "subject": "Invoice #{{invoice_number}} — {{amount}} due {{due_date}}",
        "html": """<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f8fafc;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f8fafc;padding:40px 0;">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:12px;overflow:hidden;border:1px solid #e2e8f0;">
        <!-- Header -->
        <tr><td style="padding:36px 48px;border-bottom:1px solid #e2e8f0;">
          <table width="100%"><tr>
            <td><h1 style="color:#0f172a;font-size:22px;margin:0;font-weight:800;">INVOICE</h1><p style="color:#64748b;font-size:13px;margin:4px 0 0;">#{{invoice_number}}</p></td>
            <td align="right"><p style="color:#64748b;font-size:13px;margin:0;">{{company}}</p></td>
          </tr></table>
        </td></tr>
        <!-- Billing info -->
        <tr><td style="padding:28px 48px;">
          <p style="color:#374151;font-size:15px;margin:0 0 24px;">Hi <strong>{{name}}</strong>, here is your invoice summary:</p>
          <table width="100%" style="border-collapse:collapse;">
            <tr style="background:#f1f5f9;">
              <th style="text-align:left;padding:10px 14px;color:#64748b;font-size:12px;text-transform:uppercase;letter-spacing:0.5px;">Description</th>
              <th style="text-align:right;padding:10px 14px;color:#64748b;font-size:12px;text-transform:uppercase;letter-spacing:0.5px;">Amount</th>
            </tr>
            <tr><td style="padding:12px 14px;color:#374151;font-size:14px;border-bottom:1px solid #e2e8f0;">{{description}}</td>
                <td style="padding:12px 14px;color:#374151;font-size:14px;text-align:right;border-bottom:1px solid #e2e8f0;">{{amount}}</td></tr>
            <tr style="background:#f8fafc;">
              <td style="padding:12px 14px;color:#0f172a;font-weight:700;font-size:15px;">Total Due</td>
              <td style="padding:12px 14px;color:#6366f1;font-weight:700;font-size:15px;text-align:right;">{{amount}}</td>
            </tr>
          </table>
          <p style="color:#64748b;font-size:13px;margin:20px 0 0;">Due by: <strong style="color:#ef4444;">{{due_date}}</strong></p>
        </td></tr>
        <!-- CTA -->
        <tr><td style="padding:0 48px 36px;text-align:center;">
          <a href="#" style="background:#6366f1;color:#fff;text-decoration:none;padding:13px 32px;border-radius:8px;font-size:14px;font-weight:600;display:inline-block;">Pay Now →</a>
        </td></tr>
        <!-- Footer -->
        <tr><td style="background:#f8fafc;padding:20px 48px;text-align:center;border-top:1px solid #e2e8f0;">
          <p style="color:#94a3b8;font-size:12px;margin:0;">Questions? Reply to this email or contact {{company}}.</p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>""",
        "plaintext": """Hi {{name}},

Please find your invoice details below:

Invoice #: {{invoice_number}}
Description: {{description}}
Amount Due: {{amount}}
Due Date: {{due_date}}

To pay, visit our website or reply to this email.

{{company}}"""
    },

    "follow_up": {
        "name": "Follow-up / Outreach",
        "description": "Simple, personal-looking follow-up or cold outreach email",
        "subject": "Following up — {{subject_line}}",
        "html": """<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#ffffff;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="padding:40px 0;">
    <tr><td align="center">
      <table width="560" cellpadding="0" cellspacing="0">
        <tr><td style="padding:0 0 32px;">
          <p style="color:#374151;font-size:15px;line-height:1.7;margin:0 0 16px;">Hi {{name}},</p>
          <p style="color:#374151;font-size:15px;line-height:1.7;margin:0 0 16px;">
            I wanted to follow up on my previous message about <strong>{{topic}}</strong>. I know things get busy, so I just wanted to make sure this didn't slip through the cracks.
          </p>
          <p style="color:#374151;font-size:15px;line-height:1.7;margin:0 0 16px;">{{custom_message}}</p>
          <p style="color:#374151;font-size:15px;line-height:1.7;margin:0 0 32px;">Would you have 15 minutes this week for a quick call?</p>
          <a href="#" style="background:#0f172a;color:#fff;text-decoration:none;padding:12px 28px;border-radius:6px;font-size:14px;font-weight:600;display:inline-block;">Schedule a Call</a>
        </td></tr>
        <tr><td style="padding:24px 0 0;border-top:1px solid #e5e7eb;">
          <p style="color:#374151;font-size:14px;margin:0;">Best,<br><strong>{{sender_name}}</strong><br><span style="color:#6b7280;">{{company}}</span></p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>""",
        "plaintext": """Hi {{name}},

I wanted to follow up on my previous message about {{topic}}. I know things get busy, so I just wanted to make sure this didn't slip through the cracks.

{{custom_message}}

Would you have 15 minutes this week for a quick call?

Best,
{{sender_name}}
{{company}}"""
    },
}
