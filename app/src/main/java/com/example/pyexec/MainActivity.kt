package com.example.pyexec

import android.app.AlertDialog
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Start Python (Chaquopy)
        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(this))
        }

        val input = findViewById<EditText>(R.id.codeInput)
        val resultView = findViewById<TextView>(R.id.txtResult)
        val runButton = findViewById<Button>(R.id.btnRun)

        runButton.setOnClickListener {
            val userCode = input.text.toString()

            try {
                val py = Python.getInstance()
                val script = py.getModule("script")
                val output = script.callAttr("run_code", userCode).toString()

                // Scrollable + copyable popup
                val outputTextView = TextView(this).apply {
                    text = output
                    setPadding(32, 32, 32, 32)
                    setTextIsSelectable(true)
                }

                val scrollView = ScrollView(this).apply {
                    addView(outputTextView)
                    isFillViewport = true
                }

                AlertDialog.Builder(this)
                    .setTitle("Result")
                    .setView(scrollView)
                    .setPositiveButton("Copy") { _, _ ->
                        val clipboard = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                        val clip = ClipData.newPlainText("Python Output", output)
                        clipboard.setPrimaryClip(clip)
                        Toast.makeText(this, "Copied to clipboard", Toast.LENGTH_SHORT).show()
                    }
                    .setNegativeButton("Close", null)
                    .show()

                resultView.text = "Executed successfully"
            } catch (e: Exception) {
                AlertDialog.Builder(this)
                    .setTitle("Error")
                    .setMessage(e.message)
                    .setPositiveButton("OK", null)
                    .show()
            }
        }
    }
}
