import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import QACard from './QACard';

describe('QACard Component', () => {
  const mockItem = {
    q: 'Test Question?',
    a: 'Test Answer.',
    table: 'Test Table Data'
  };

  it('renders the question and answer correctly', () => {
    render(<QACard item={mockItem} index={0} />);
    
    // Check if question is rendered (Q1 because index is 0)
    expect(screen.getByText('Q1: Test Question?')).toBeInTheDocument();
    
    // Check if answer is rendered
    expect(screen.getByText('Test Answer.')).toBeInTheDocument();
  });

  it('renders the table data when provided', () => {
    render(<QACard item={mockItem} index={1} />);
    
    // Q2 because index is 1
    expect(screen.getByText('Q2: Test Question?')).toBeInTheDocument();
    expect(screen.getByText('Test Table Data')).toBeInTheDocument();
  });

  it('does not render a pre-formatted block if no table data is provided', () => {
    const noTableItem = { q: 'No Table?', a: 'Nope.' };
    const { container } = render(<QACard item={noTableItem} index={0} />);
    
    expect(screen.getByText('Q1: No Table?')).toBeInTheDocument();
    expect(screen.getByText('Nope.')).toBeInTheDocument();
    
    // Check that pre-formatted block doesn't exist
    expect(container.querySelector('.pre-formatted')).not.toBeInTheDocument();
  });
});
